#!/usr/bin/env python3
import math
import time
import subprocess

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from gazebo_ros_link_attacher.srv import Attach

# ✅ NEW (ARM ONLY): TF for precise end-effector pose
import tf2_ros
from rclpy.duration import Duration


def yaw_from_quat(x, y, z, w):
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)


def wrap_to_pi(a):
    while a > math.pi:
        a -= 2.0 * math.pi
    while a < -math.pi:
        a += 2.0 * math.pi
    return a


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def quat_mul(q1, q2):
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2
    return (
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
    )


def quat_conj(q):
    x, y, z, w = q
    return (-x, -y, -z, w)


def quat_rotate(q, v):
    # rotate vector v by quaternion q
    vx, vy, vz = v
    qv = (vx, vy, vz, 0.0)
    qr = quat_mul(quat_mul(q, qv), quat_conj(q))
    return (qr[0], qr[1], qr[2])


class ScenarioCoordinator(Node):
    def __init__(self):
        super().__init__("scenario_coordinator")

        # ---------------- params ----------------
        self.odom_topic = self.declare_parameter("odom_topic", "/odom").value
        self.scan_topic = self.declare_parameter("scan_topic", "/tb3/scan").value
        self.cmd_vel_topic = self.declare_parameter("cmd_vel_topic", "/cmd_vel").value

        self.attach_service = self.declare_parameter("attach_service", "/attach").value
        self.detach_service = self.declare_parameter("detach_service", "/detach").value

        self.tb3_model = self.declare_parameter("tb3_model", "tb3").value
        self.tb3_link = self.declare_parameter("tb3_link", "tb3::base_link").value
        self.stone_model = self.declare_parameter("stone_model", "stone").value
        self.stone_link = self.declare_parameter("stone_link", "stone::stone_link").value

        stone_xy = self.declare_parameter("stone_xy", [3.45662, -0.223026]).value
        arm_xy = self.declare_parameter("arm_xy", [-1.3, -0.3]).value
        container_xy = self.declare_parameter("container_xy", [-1.54015, -1.08473]).value

        self.stone_xy = (float(stone_xy[0]), float(stone_xy[1]))
        self.arm_xy = (float(arm_xy[0]), float(arm_xy[1]))
        self.container_xy = (float(container_xy[0]), float(container_xy[1]))

        obs_box = self.declare_parameter("obstacle_box_xy", [1.51611, -3.24702]).value
        obs_cyl = self.declare_parameter("obstacle_cyl_xy", [2.87436, -2.43085]).value
        self.obstacle_box_xy = (float(obs_box[0]), float(obs_box[1]))
        self.obstacle_cyl_xy = (float(obs_cyl[0]), float(obs_cyl[1]))

        # speeds
        self.v_go = float(self.declare_parameter("v_go", 0.30).value)
        self.v_touch = float(self.declare_parameter("v_touch", 0.08).value)
        self.v_push = float(self.declare_parameter("v_push", 0.22).value)
        self.w_max = float(self.declare_parameter("w_max", 1.2).value)

        # attach / detach
        self.attach_dist = float(self.declare_parameter("attach_dist", 0.14).value)
        self.attach_center_tol_deg = float(self.declare_parameter("attach_center_tol_deg", 4.0).value)
        self.arm_drop_offset_x = float(self.declare_parameter("arm_drop_offset_x", 0.25).value)
        self.arm_stop_dist = float(self.declare_parameter("arm_stop_dist", 0.22).value)

        # When stone attached it sits in front and ruins front obstacle check.
        self.front_ignore_if_attached = 0.28

        # timers / timeouts
        self.touch_timeout = 35.0
        self.push_timeout = 55.0
        self.service_timeout = 6.0

        # ---------------- ROS I/O ----------------
        self.pub_cmd = self.create_publisher(Twist, self.cmd_vel_topic, 10)
        self.pub_status = self.create_publisher(String, "/scenario_status", 10)
        self.pub_traj = self.create_publisher(JointTrajectory, "/iiwa_arm_controller/joint_trajectory", 10)

        self.sub_odom = self.create_subscription(Odometry, self.odom_topic, self.cb_odom, 10)
        self.sub_scan = self.create_subscription(LaserScan, self.scan_topic, self.cb_scan, 10)

        self.cli_attach = self.create_client(Attach, self.attach_service)
        self.cli_detach = self.create_client(Attach, self.detach_service)

        # ---------------- state ----------------
        self.x = None
        self.y = None
        self.yaw = None
        self.scan = None

        self.state = "INIT"
        self.state_t0 = time.time()

        self.attached = False
        self.attach_future = None
        self.detach_future = None
        self.req_sent_t = 0.0

        self.arm_started_t = None
        self.start_pose = None  # for return home

        # stuck detector
        self._last_stuck_check_t = time.time()
        self._last_stuck_pose = None
        self._last_cmd = Twist()

        # ===================== ARM GRASP CONFIG =====================
        self.arm_model = self.declare_parameter("arm_model", "lbr_iiwa").value
        self.arm_ee_link = self.declare_parameter("arm_ee_link", "lbr_iiwa::lbr_iiwa_link_7").value

        # stone pick point (after tb3 detach)
        self.stone_pick_xy = self.declare_parameter("stone_pick_xy", [-1.05, -0.30]).value
        self.stone_pick_xy = (float(self.stone_pick_xy[0]), float(self.stone_pick_xy[1]))

        self.stone_z_ground = float(self.declare_parameter("stone_z_ground", 0.08).value)
        self.stone_z_carry  = float(self.declare_parameter("stone_z_carry", 0.32).value)

        # fallback grasp pose (world coords)
        gp = self.declare_parameter("grasp_pose_xyz", [-1.05, -0.30, 0.32]).value
        self.grasp_pose_xyz = (float(gp[0]), float(gp[1]), float(gp[2]))
        self.grasp_yaw = float(self.declare_parameter("grasp_yaw", 0.0).value)

        # place pose (world coords)
        pp = self.declare_parameter("place_pose_xyz", [-1.54015, -1.08473, 0.12]).value
        self.place_pose_xyz = (float(pp[0]), float(pp[1]), float(pp[2]))
        self.place_yaw = float(self.declare_parameter("place_yaw", 0.0).value)

        # ✅ NEW: tiny offset from EE so stone sits “inside mouth”
        # اگر هنوز فاصله داشت: x رو کم/زیاد کن (مثلاً 0.04 تا 0.10)
        off = self.declare_parameter("ee_offset_xyz", [0.06, 0.00, 0.00]).value
        self.ee_offset_xyz = (float(off[0]), float(off[1]), float(off[2]))

        # ✅ NEW: TF frames (world frame in Gazebo classic is usually "world")
        self.world_frame = self.declare_parameter("world_frame", "world").value
        self.ee_frame = self.declare_parameter("ee_frame", "lbr_iiwa_link_7").value

        self._arm_grasped = False
        self._arm_released = False
        self._arm_attach_future = None
        self._arm_detach_future = None

        # ✅ NEW (ARM ONLY): TF buffer/listener
        self.tf_buffer = tf2_ros.Buffer(cache_time=Duration(seconds=5.0))
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        # ============================================================

        self.timer = self.create_timer(0.05, self.loop)  # 20Hz
        self.set_status("INIT")
        self.get_logger().info("ScenarioCoordinator started.")

    # ---------------- callbacks ----------------
    def cb_odom(self, msg: Odometry):
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        self.x = p.x
        self.y = p.y
        self.yaw = yaw_from_quat(q.x, q.y, q.z, q.w)
        if self.start_pose is None:
            self.start_pose = (self.x, self.y)

    def cb_scan(self, msg: LaserScan):
        self.scan = msg

    # ---------------- helper: status/state ----------------
    def set_status(self, s: str):
        self.state = s
        self.state_t0 = time.time()
        m = String()
        m.data = s
        try:
            self.pub_status.publish(m)
        except Exception:
            pass
        self.get_logger().info(f"STATUS: {s}")

    def elapsed(self):
        return time.time() - self.state_t0

    # ---------------- helper: motion ----------------
    def stop(self):
        t = Twist()
        self.pub_cmd.publish(t)
        self._last_cmd = t

    def stop_hard(self, n=12, dt=0.02):
        t = Twist()
        for _ in range(n):
            self.pub_cmd.publish(t)
            time.sleep(dt)
        self._last_cmd = t

    def drive(self, v, w):
        t = Twist()
        t.linear.x = float(v)
        t.angular.z = float(w)
        self.pub_cmd.publish(t)
        self._last_cmd = t

    # ---------------- LiDAR helpers ----------------
    def scan_min_window(self, center_rad, half_width_rad):
        if self.scan is None:
            return float("inf")
        msg = self.scan
        best = float("inf")
        ang = msg.angle_min
        for r in msg.ranges:
            if math.isfinite(r) and msg.range_min < r < msg.range_max:
                a = wrap_to_pi(ang)
                if abs(wrap_to_pi(a - center_rad)) <= half_width_rad:
                    if self.attached:
                        if abs(a) < math.radians(25.0) and r < 0.45:
                            ang += msg.angle_increment
                            continue
                    best = min(best, r)
            ang += msg.angle_increment
        return best

    def closest_in_front(self, win_deg=18.0):
        if self.scan is None:
            return None
        msg = self.scan
        win = math.radians(win_deg)
        best_r, best_a = None, None
        ang = msg.angle_min
        for r in msg.ranges:
            if math.isfinite(r) and msg.range_min < r < msg.range_max:
                a = wrap_to_pi(ang)
                if abs(a) <= win:
                    if best_r is None or r < best_r:
                        best_r, best_a = r, a
            ang += msg.angle_increment
        if best_r is None:
            return None
        return best_r, best_a

    # ---------------- avoidance ----------------
    def avoidance(self, desired_v, desired_w):
        front = self.scan_min_window(0.0, math.radians(18))
        fl = self.scan_min_window(+math.radians(35), math.radians(15))
        fr = self.scan_min_window(-math.radians(35), math.radians(15))
        left = self.scan_min_window(+math.radians(90), math.radians(20))
        right = self.scan_min_window(-math.radians(90), math.radians(20))

        if self.attached and front < self.front_ignore_if_attached:
            front = 9.9

        v = desired_v
        w = desired_w

        stop_d = 0.28
        slow_d = 0.55

        if front < stop_d or fl < 0.22 or fr < 0.22:
            v = 0.0
            w = -0.95 if fl < fr else +0.95
            return v, w

        if front < slow_d or fl < 0.40 or fr < 0.40:
            v = min(v, 0.12)

        rep = 0.0
        if fl < 0.65:
            rep -= (0.65 - fl) * 1.2
        if fr < 0.65:
            rep += (0.65 - fr) * 1.2
        if left < 0.55:
            rep -= (0.55 - left) * 0.8
        if right < 0.55:
            rep += (0.55 - right) * 0.8

        w = clamp(w + rep, -1.3, 1.3)
        v = clamp(v, 0.0, 0.34)
        return v, w

    # ---------------- go-to controller ----------------
    def go_to(self, xy, stop_dist=0.55, v_nom=0.28):
        dx = xy[0] - self.x
        dy = xy[1] - self.y
        d = math.hypot(dx, dy)
        if d < stop_dist:
            self.stop_hard(n=6, dt=0.02)
            return True

        target = math.atan2(dy, dx)
        err = wrap_to_pi(target - self.yaw)

        desired_w = clamp(1.25 * err, -self.w_max, self.w_max)
        desired_v = v_nom * (1.0 - min(1.0, abs(err)))
        desired_v = max(0.08, desired_v)

        v, w = self.avoidance(desired_v, desired_w)
        self.drive(v, w)
        return False

    # ---------------- recovery ----------------
    def is_stuck(self):
        now = time.time()
        if now - self._last_stuck_check_t < 3.0:
            return False
        if self._last_stuck_pose is None:
            self._last_stuck_pose = (self.x, self.y)
            self._last_stuck_check_t = now
            return False
        moved = math.hypot(self.x - self._last_stuck_pose[0], self.y - self._last_stuck_pose[1])
        self._last_stuck_pose = (self.x, self.y)
        self._last_stuck_check_t = now
        forward_cmd = self._last_cmd.linear.x > 0.10
        return forward_cmd and moved < 0.04

    def do_recovery(self):
        t = self.elapsed()
        if t < 0.7:
            self.drive(-0.12, 0.0); return
        if t < 1.8:
            self.drive(0.0, 0.95); return
        if t < 2.6:
            self.drive(+0.12, 0.0); return
        self.stop_hard(n=8, dt=0.02)
        self.set_status("TB3_PUSH_TO_ARM" if self.attached else "TB3_GOTO_STONE_AREA")

    # ---------------- attach/detach services ----------------
    def make_req(self):
        req = Attach.Request()
        req.model_name_1 = self.tb3_model
        req.link_name_1 = self.tb3_link
        req.model_name_2 = self.stone_model
        req.link_name_2 = self.stone_link
        return req

    def start_attach(self):
        if self.attach_future is not None:
            return
        if not self.cli_attach.service_is_ready():
            self.get_logger().warn("attach service not ready yet...")
            return
        self.req_sent_t = time.time()
        self.attach_future = self.cli_attach.call_async(self.make_req())
        self.get_logger().info("Attach request sent (async).")

    def start_detach(self):
        if self.detach_future is not None:
            return
        if not self.cli_detach.service_is_ready():
            self.get_logger().warn("detach service not ready yet...")
            return
        self.req_sent_t = time.time()
        self.detach_future = self.cli_detach.call_async(self.make_req())
        self.get_logger().info("Detach request sent (async).")

    # ---------------- Gazebo pose modify (for stone) ----------------
    def gz_set_model_pose(self, model_name: str, x: float, y: float, z: float, yaw: float = 0.0):
        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)
        topic = f"/gazebo/lab_world/pose/modify"
        msg = (
            f"name: '{model_name}' "
            f"position {{ x: {x} y: {y} z: {z} }} "
            f"orientation {{ x: 0 y: 0 z: {qz} w: {qw} }}"
        )
        cmd = ["gz", "topic", "-t", topic, "-m", "gazebo.msgs.Pose", "-p", msg]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False

    # ✅ NEW (ARM ONLY): get EE pose in world via TF (fallback to manual)
    def get_ee_world_pose(self):
        try:
            tf = self.tf_buffer.lookup_transform(
                self.world_frame, self.ee_frame, rclpy.time.Time(),
                timeout=Duration(seconds=0.15)
            )
            tx = tf.transform.translation.x
            ty = tf.transform.translation.y
            tz = tf.transform.translation.z
            qx = tf.transform.rotation.x
            qy = tf.transform.rotation.y
            qz = tf.transform.rotation.z
            qw = tf.transform.rotation.w
            q = (qx, qy, qz, qw)

            # offset in EE frame -> world
            ox, oy, oz = quat_rotate(q, self.ee_offset_xyz)
            return (tx + ox, ty + oy, tz + oz, q)
        except Exception:
            return None

    # ---------------- arm trajectory ----------------
    def send_arm_pick_place(self):
        jt = JointTrajectory()
        jt.joint_names = [
            "lbr_iiwa_joint_1", "lbr_iiwa_joint_2", "lbr_iiwa_joint_3",
            "lbr_iiwa_joint_4", "lbr_iiwa_joint_5", "lbr_iiwa_joint_6", "lbr_iiwa_joint_7"
        ]

        def pt(pos, sec):
            p = JointTrajectoryPoint()
            p.positions = pos
            p.time_from_start.sec = sec
            return p

        home      = [0.0,  0.4, 0.0, -1.2, 0.0,  1.0, 0.0]
        pre_pick  = [0.2,  0.9, 0.0, -1.7, 0.0,  1.2, 0.0]
        lift      = [0.2,  0.3, 0.0, -1.1, 0.0,  1.0, 0.0]
        pre_place = [-0.4, 0.7, 0.0, -1.3, 0.0,  1.1, 0.0]
        place     = [-0.45,0.55,0.0, -1.35,0.0,  1.05,0.0]

        jt.points = [pt(home, 2), pt(pre_pick, 5), pt(lift, 8), pt(pre_place, 12), pt(place, 14), pt(home, 18)]
        self.pub_traj.publish(jt)

    # ---------------- main loop ----------------
    def loop(self):
        if self.x is None or self.scan is None:
            return

        if self.state in ("TB3_GOTO_STONE_AREA", "TB3_TOUCH_AND_ATTACH", "TB3_PUSH_TO_ARM", "TB3_GOTO_HOME"):
            if self.is_stuck():
                self.get_logger().warn("TB3 seems stuck -> RECOVERY")
                self.set_status("RECOVERY")
                return

        if self.state == "INIT":
            self.attached = False
            self.attach_future = None
            self.detach_future = None
            self.arm_started_t = None
            self._last_stuck_pose = (self.x, self.y)
            self._last_stuck_check_t = time.time()
            self.set_status("TB3_GOTO_STONE_AREA")
            return

        if self.state == "TB3_GOTO_STONE_AREA":
            if self.go_to(self.stone_xy, stop_dist=0.85, v_nom=self.v_go):
                self.set_status("TB3_TOUCH_AND_ATTACH")
            return

        if self.state == "TB3_TOUCH_AND_ATTACH":
            if self.elapsed() > self.touch_timeout:
                self.get_logger().warn("Touch timeout -> go_to stone area again")
                self.set_status("TB3_GOTO_STONE_AREA")
                return

            obj = self.closest_in_front(18.0)
            if obj is None:
                self.drive(0.0, 0.35)
                return

            r, a = obj

            if abs(a) > math.radians(8.0):
                self.drive(0.0, clamp(1.6 * a, -0.75, 0.75))
                return

            if (r <= self.attach_dist) and (abs(a) <= math.radians(self.attach_center_tol_deg)):
                self.stop_hard(n=14, dt=0.02)
                self.set_status("ATTACH")
                return

            self.drive(self.v_touch, clamp(0.9 * a, -0.35, 0.35))
            return

        if self.state == "ATTACH":
            self.stop_hard(n=10, dt=0.02)
            self.start_attach()

            if self.attach_future is None:
                return

            if self.attach_future.done():
                res = self.attach_future.result()
                self.attach_future = None
                ok = (res is not None and bool(res.ok))
                self.get_logger().info(f"ATTACH result ok={ok}")

                if ok:
                    self.attached = True
                    self.stop_hard(n=16, dt=0.02)
                    self.set_status("TB3_PUSH_TO_ARM")
                else:
                    self.set_status("TB3_TOUCH_AND_ATTACH")
                return

            if (time.time() - self.req_sent_t) > self.service_timeout:
                self.get_logger().warn("ATTACH timeout -> retry touch")
                self.attach_future = None
                self.set_status("TB3_TOUCH_AND_ATTACH")
            return

        if self.state == "TB3_PUSH_TO_ARM":
            if self.elapsed() > self.push_timeout:
                self.get_logger().warn("Push timeout -> try detach anyway near arm")
                self.set_status("TB3_DETACH_NEAR_ARM")
                return

            drop_xy = (self.arm_xy[0] + self.arm_drop_offset_x, self.arm_xy[1])
            if self.go_to(drop_xy, stop_dist=self.arm_stop_dist, v_nom=self.v_push):
                self.set_status("TB3_DETACH_NEAR_ARM")
            return

        if self.state == "TB3_DETACH_NEAR_ARM":
            self.stop_hard(n=18, dt=0.02)
            self.start_detach()

            if self.detach_future is None:
                return

            if self.detach_future.done():
                res = self.detach_future.result()
                self.detach_future = None
                ok = (res is not None and bool(res.ok))
                self.get_logger().info(f"DETACH result ok={ok}")

                if ok:
                    self.attached = False
                    self.stop_hard(n=18, dt=0.02)

                    # fix stone exactly at pick point for arm (ground)
                    self.gz_set_model_pose(self.stone_model, self.stone_pick_xy[0], self.stone_pick_xy[1], self.stone_z_ground, yaw=0.0)
                    time.sleep(0.05)
                    self.gz_set_model_pose(self.stone_model, self.stone_pick_xy[0], self.stone_pick_xy[1], self.stone_z_ground, yaw=0.0)

                    self.set_status("ARM_PICK_PLACE")
                else:
                    self.set_status("TB3_DETACH_NEAR_ARM")
                return

            if (time.time() - self.req_sent_t) > self.service_timeout:
                self.get_logger().warn("DETACH timeout -> retry")
                self.detach_future = None
            return

        # ✅ ARM section (ONLY CHANGED HERE)
        if self.state == "ARM_PICK_PLACE":
            self.stop()

            # 1) wait until controller subscribes, then publish trajectory multiple times
            if self.arm_started_t is None:
                subs = self.pub_traj.get_subscription_count()
                if subs <= 0:
                    self.get_logger().warn("Waiting for /iiwa_arm_controller/joint_trajectory subscriber...")
                    return

                self.arm_started_t = time.time()

                # publish several times (robust)
                for _ in range(5):
                    self.send_arm_pick_place()
                    time.sleep(0.03)

                self.get_logger().info("Arm trajectory published (robust x5).")
                self._arm_grasped = False
                self._arm_released = False
                self._arm_attach_future = None
                self._arm_detach_future = None

            t = time.time() - self.arm_started_t

            # --- (A) PRE-GRASP: snap stone into EE mouth using TF if possible (fallback to grasp_pose_xyz) ---
            if 4.2 < t < 4.9 and (not self._arm_grasped):
                ee = self.get_ee_world_pose()
                if ee is not None:
                    ex, ey, ez, q = ee
                    # keep a bit above to avoid ground collision
                    self.gz_set_model_pose(self.stone_model, ex, ey, max(ez, self.stone_z_carry), yaw=self.grasp_yaw)
                else:
                    self.gz_set_model_pose(
                        self.stone_model,
                        self.grasp_pose_xyz[0], self.grasp_pose_xyz[1], self.grasp_pose_xyz[2],
                        yaw=self.grasp_yaw
                    )

            # --- (B) GRASP: attach stone to ee link ---
            if (4.9 < t < 7.0) and (not self._arm_grasped):
                req = Attach.Request()
                req.model_name_1 = self.arm_model
                req.link_name_1 = self.arm_ee_link
                req.model_name_2 = self.stone_model
                req.link_name_2 = self.stone_link
                if self.cli_attach.service_is_ready():
                    self._arm_attach_future = self.cli_attach.call_async(req)
                    self._arm_grasped = True
                    self.get_logger().info("ARM_GRASP: attach stone -> ee requested")

            # --- (C) HOLD TIGHT: keep stone glued to EE (visual + prevents offset drift) ---
            if self._arm_grasped and (7.0 < t < 12.0):
                ee = self.get_ee_world_pose()
                if ee is not None:
                    ex, ey, ez, q = ee
                    self.gz_set_model_pose(self.stone_model, ex, ey, max(ez, self.stone_z_carry), yaw=self.grasp_yaw)
                else:
                    self.gz_set_model_pose(
                        self.stone_model,
                        self.grasp_pose_xyz[0], self.grasp_pose_xyz[1], self.stone_z_carry,
                        yaw=self.grasp_yaw
                    )

            # --- (D) RELEASE: place on container, then detach ---
            if (13.0 < t < 15.5) and (not self._arm_released):
                self.gz_set_model_pose(
                    self.stone_model,
                    self.place_pose_xyz[0], self.place_pose_xyz[1], self.place_pose_xyz[2],
                    yaw=self.place_yaw
                )
                time.sleep(0.02)
                self.gz_set_model_pose(
                    self.stone_model,
                    self.place_pose_xyz[0], self.place_pose_xyz[1], self.place_pose_xyz[2],
                    yaw=self.place_yaw
                )

                req = Attach.Request()
                req.model_name_1 = self.arm_model
                req.link_name_1 = self.arm_ee_link
                req.model_name_2 = self.stone_model
                req.link_name_2 = self.stone_link
                if self.cli_detach.service_is_ready():
                    self._arm_detach_future = self.cli_detach.call_async(req)
                    self._arm_released = True
                    self.get_logger().info("ARM_RELEASE: detach stone from ee requested")

            # end (exactly as you requested)
            if t > 20.0:
                self.set_status("TB3_GOTO_HOME")
            return

        if self.state == "TB3_GOTO_HOME":
            if self.start_pose is None:
                self.set_status("DONE")
                return
            if self.go_to(self.start_pose, stop_dist=0.35, v_nom=self.v_go):
                self.set_status("DONE")
            return

        if self.state == "RECOVERY":
            self.do_recovery()
            return

        if self.state == "DONE":
            self.stop()
            return


def main():
    rclpy.init()
    node = ScenarioCoordinator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    try:
        node.stop_hard(n=6, dt=0.02)
        node.stop()
    except Exception:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

