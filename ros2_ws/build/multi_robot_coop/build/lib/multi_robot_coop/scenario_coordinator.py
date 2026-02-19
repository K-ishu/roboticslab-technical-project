#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from gazebo_ros_link_attacher.srv import Attach


# ---------------- math utils ----------------
def yaw_from_quat(x, y, z, w):
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def wrap_to_pi(a):
    while a > math.pi:
        a -= 2.0 * math.pi
    while a < -math.pi:
        a += 2.0 * math.pi
    return a


class ScenarioCoordinator(Node):
    """
    TB3:
      /odom
      /tb3/scan
      publish /cmd_vel   (tb3_diff_drive subscribes to this)

    Gazebo link attacher:
      /attach  gazebo_ros_link_attacher/srv/Attach
      /detach  gazebo_ros_link_attacher/srv/Attach

    Arm:
      publish /iiwa_arm_controller/joint_trajectory
    """

    def __init__(self):
        super().__init__("scenario_coordinator")

        # ===================== PARAMS =====================
        # Topics
        self.odom_topic = self.declare_parameter("odom_topic", "/odom").value
        self.scan_topic = self.declare_parameter("scan_topic", "/tb3/scan").value
        self.cmd_vel_topic = self.declare_parameter("cmd_vel_topic", "/cmd_vel").value

        # World / names for link attacher
        self.tb3_model = self.declare_parameter("tb3_model", "tb3").value
        self.tb3_link  = self.declare_parameter("tb3_link", "tb3::base_link").value
        self.stone_model = self.declare_parameter("stone_model", "stone").value
        self.stone_link  = self.declare_parameter("stone_link", "stone::stone_link").value

        # Targets
        self.stone_xy = tuple(self.declare_parameter("stone_xy", [3.45662, -0.223026]).value)
        self.arm_zone_xy = tuple(self.declare_parameter("arm_zone_xy", [-1.3, -0.3]).value)
        self.container_xy = tuple(self.declare_parameter("container_xy", [-1.54015, -1.08473]).value)

        # Stop distances
        self.goto_stone_stop = float(self.declare_parameter("goto_stone_stop", 0.85).value)
        self.arm_stop_dist   = float(self.declare_parameter("arm_stop_dist", 0.22).value)

        # --- LiDAR touch / attach tuning ---
        # فاصله واقعی که باید به سنگ برسی تا attach کنیم (gap کمتر => attach بهتر)
        self.attach_dist = float(self.declare_parameter("attach_dist", 0.16).value)  # meters
        self.attach_center_tol_deg = float(self.declare_parameter("attach_center_tol_deg", 3.0).value)

        self.lock_win_deg = float(self.declare_parameter("lock_win_deg", 18.0).value)
        self.turn_only_deg = float(self.declare_parameter("turn_only_deg", 7.0).value)

        # Speeds
        self.v_go   = float(self.declare_parameter("v_go", 0.30).value)
        self.v_touch= float(self.declare_parameter("v_touch", 0.10).value)
        self.v_push = float(self.declare_parameter("v_push", 0.22).value)

        self.w_max = float(self.declare_parameter("w_max", 1.2).value)
        self.w_touch_max = float(self.declare_parameter("w_touch_max", 0.9).value)

        # Safety / avoidance
        self.stop_front = float(self.declare_parameter("stop_front", 0.26).value)
        self.slow_front = float(self.declare_parameter("slow_front", 0.52).value)

        # Timeouts
        self.touch_timeout = float(self.declare_parameter("touch_timeout", 30.0).value)
        self.attach_timeout = float(self.declare_parameter("attach_timeout", 4.0).value)
        self.detach_timeout = float(self.declare_parameter("detach_timeout", 4.0).value)

        # Arm timing
        self.arm_total_time = float(self.declare_parameter("arm_total_time", 18.0).value)

        # ===================== ROS I/O =====================
        self.pub_cmd = self.create_publisher(Twist, self.cmd_vel_topic, 10)
        self.pub_status = self.create_publisher(String, "/scenario_status", 10)
        self.pub_traj = self.create_publisher(JointTrajectory, "/iiwa_arm_controller/joint_trajectory", 10)

        self.sub_odom = self.create_subscription(Odometry, self.odom_topic, self.cb_odom, 10)
        self.sub_scan = self.create_subscription(LaserScan, self.scan_topic, self.cb_scan, 10)

        self.cli_attach = self.create_client(Attach, "/attach")
        self.cli_detach = self.create_client(Attach, "/detach")

        # ===================== STATE =====================
        self.x = None
        self.y = None
        self.yaw = None
        self.scan = None

        self.state = "INIT"
        self.state_t0 = time.time()

        self.attached = False

        # async futures
        self.attach_future = None
        self.detach_future = None
        self.req_sent_t = 0.0

        # for arm
        self.arm_started_t = None
        self.arm_sent_once = False

        # track stuck
        self._last_pose_t = time.time()
        self._last_pose_xy = None

        # loop
        self.timer = self.create_timer(0.05, self.loop)  # 20 Hz

        self._set_state("INIT")
        self.get_logger().info(
            f"ScenarioCoordinator started. cmd_vel={self.cmd_vel_topic}, odom={self.odom_topic}, scan={self.scan_topic}"
        )

    # ---------------- callbacks ----------------
    def cb_odom(self, msg: Odometry):
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        self.x = p.x
        self.y = p.y
        self.yaw = yaw_from_quat(q.x, q.y, q.z, q.w)

    def cb_scan(self, msg: LaserScan):
        self.scan = msg

    # ---------------- helpers ----------------
    def _set_state(self, s: str):
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

    def stop(self):
        try:
            if not rclpy.ok():
                return
            self.pub_cmd.publish(Twist())
        except Exception:
            pass

    def stop_hard(self, n=10, dt=0.02):
        """چند بار صفر بده تا ربات/سنگ بعد attach/detach نچرخه"""
        try:
            if not rclpy.ok():
                return
            z = Twist()
            for _ in range(n):
                self.pub_cmd.publish(z)
                time.sleep(dt)
        except Exception:
            pass

    def drive(self, v, w):
        t = Twist()
        t.linear.x = float(v)
        t.angular.z = float(w)
        try:
            self.pub_cmd.publish(t)
        except Exception:
            pass

    def dist_to(self, xy):
        if self.x is None:
            return 1e9
        return math.hypot(self.x - xy[0], self.y - xy[1])

    # ---------------- LiDAR helpers ----------------
    def scan_min_window(self, center_rad, half_width_rad):
        if self.scan is None:
            return float("inf")
        msg = self.scan
        ang = msg.angle_min
        best = float("inf")
        for r in msg.ranges:
            if math.isfinite(r) and msg.range_min < r < msg.range_max:
                a = wrap_to_pi(ang)
                if abs(wrap_to_pi(a - center_rad)) <= half_width_rad:
                    best = min(best, r)
            ang += msg.angle_increment
        return best

    def closest_in_front(self, win_deg=18.0):
        """closest point within +/- win_deg in front, returns (range, angle)"""
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
    def compute_avoid(self, desired_v, desired_w):
        front = self.scan_min_window(0.0, math.radians(18))
        left  = self.scan_min_window(+math.radians(60), math.radians(20))
        right = self.scan_min_window(-math.radians(60), math.radians(20))

        v = desired_v
        w = desired_w

        if front < self.stop_front:
            v = 0.0
            w = +0.9 if left > right else -0.9
            return v, w

        if front < self.slow_front:
            v = min(v, 0.12)

        side = 0.0
        if left < 0.60:
            side -= (0.60 - left) * 0.9
        if right < 0.60:
            side += (0.60 - right) * 0.9

        w = clamp(w + side, -1.3, 1.3)
        v = clamp(v, 0.0, 0.30)
        return v, w

    # ---------------- go-to ----------------
    def go_to(self, xy, stop_dist):
        dx = xy[0] - self.x
        dy = xy[1] - self.y
        d = math.hypot(dx, dy)

        if d < stop_dist:
            self.stop_hard(n=5, dt=0.02)
            return True

        target = math.atan2(dy, dx)
        err = wrap_to_pi(target - self.yaw)

        w = clamp(1.3 * err, -self.w_max, self.w_max)
        v = self.v_go * (1.0 - min(1.0, abs(err)))
        v = max(0.10, v)  # سرعت پایه بالاتر

        v, w = self.compute_avoid(v, w)
        self.drive(v, w)
        return False

    # ---------------- stuck detector ----------------
    def is_stuck(self):
        """اگر در 3 ثانیه، کمتر از 3cm حرکت کرده باشد در حالی که باید جلو برود."""
        if self.x is None:
            return False
        now = time.time()
        if now - self._last_pose_t < 3.0:
            return False
        if self._last_pose_xy is None:
            self._last_pose_xy = (self.x, self.y)
            self._last_pose_t = now
            return False
        moved = math.hypot(self.x - self._last_pose_xy[0], self.y - self._last_pose_xy[1])
        self._last_pose_xy = (self.x, self.y)
        self._last_pose_t = now
        return moved < 0.03

    def recovery(self):
        t = self.elapsed()
        if t < 0.8:
            self.drive(-0.12, 0.0); return
        if t < 1.8:
            self.drive(0.0, 0.95); return
        if t < 2.5:
            self.drive(+0.10, 0.0); return
        self.stop_hard(n=4, dt=0.02)
        self._set_state("TB3_GOTO_STONE")

    # ---------------- attach/detach services ----------------
    def _make_req(self):
        req = Attach.Request()
        req.model_name_1 = self.tb3_model
        req.link_name_1  = self.tb3_link
        req.model_name_2 = self.stone_model
        req.link_name_2  = self.stone_link
        return req

    def _start_attach(self):
        if self.attach_future is not None:
            return
        if not self.cli_attach.service_is_ready():
            self.get_logger().warn("attach service not ready yet...")
            return
        self.req_sent_t = time.time()
        self.attach_future = self.cli_attach.call_async(self._make_req())
        self.get_logger().info("Attach request sent.")

    def _start_detach(self):
        if self.detach_future is not None:
            return
        if not self.cli_detach.service_is_ready():
            self.get_logger().warn("detach service not ready yet...")
            return
        self.req_sent_t = time.time()
        self.detach_future = self.cli_detach.call_async(self._make_req())
        self.get_logger().info("Detach request sent.")

    # ---------------- arm command ----------------
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

        jt.points = [
            pt(home, 2),
            pt(pre_pick, 5),
            pt(lift, 8),
            pt(pre_place, 12),
            pt(place, 14),
            pt(home, 18),
        ]
        try:
            self.pub_traj.publish(jt)
        except Exception:
            pass

    # ---------------- main loop ----------------
    def loop(self):
        if self.x is None or self.scan is None:
            return

        # اگر در مراحل کلیدی گیر کرد
        if self.state in ("TB3_GOTO_STONE", "TB3_TOUCH", "TB3_GOTO_ARM"):
            if self.is_stuck():
                self.get_logger().warn("TB3 seems stuck -> RECOVERY")
                self._set_state("RECOVERY")
                return

        if self.state == "INIT":
            self.attached = False
            self.attach_future = None
            self.detach_future = None
            self.arm_started_t = None
            self.arm_sent_once = False
            self._set_state("TB3_GOTO_STONE")
            return

        if self.state == "RECOVERY":
            self.recovery()
            return

        # 1) go to stone area
        if self.state == "TB3_GOTO_STONE":
            if self.go_to(self.stone_xy, stop_dist=self.goto_stone_stop):
                self._set_state("TB3_TOUCH")
            return

        # 2) lidar lock + touch to make attach reliable
        if self.state == "TB3_TOUCH":
            # timeout -> retry go_to
            if self.elapsed() > self.touch_timeout:
                self.get_logger().warn("Touch timeout -> go_to stone again")
                self._set_state("TB3_GOTO_STONE")
                return

            obj = self.closest_in_front(self.lock_win_deg)
            if obj is None:
                # rotate slowly to search
                self.drive(0.0, 0.30)
                return

            r, a = obj

            # safety
            if self.scan_min_window(0.0, math.radians(15)) < 0.22:
                self.stop_hard(n=5, dt=0.02)
                return

            # if close enough and centered => ATTACH
            if (r < self.attach_dist) and (abs(a) < math.radians(self.attach_center_tol_deg)):
                self.stop_hard(n=12, dt=0.02)
                self._set_state("ATTACH")
                return

            # off-center => rotate only
            if abs(a) > math.radians(self.turn_only_deg):
                self.drive(0.0, clamp(1.8 * a, -self.w_touch_max, self.w_touch_max))
                return

            # forward slow, with small correction
            v = self.v_touch
            if r < 0.55:
                v = 0.08
            self.drive(v, clamp(1.0 * a, -0.45, 0.45))
            return

        # 3) attach (async) + strict wait
        if self.state == "ATTACH":
            self.stop_hard(n=8, dt=0.02)
            self._start_attach()

            if self.attach_future is None:
                return

            if self.attach_future.done():
                res = None
                try:
                    res = self.attach_future.result()
                except Exception:
                    res = None
                self.attach_future = None

                ok = (res is not None and bool(res.ok))
                self.get_logger().info(f"ATTACH done ok={ok}")

                if ok:
                    self.attached = True
                    # stop hard to prevent spinning
                    self.stop_hard(n=14, dt=0.02)
                    self._set_state("TB3_GOTO_ARM")
                else:
                    # retry touch
                    self._set_state("TB3_TOUCH")
                return

            if (time.time() - self.req_sent_t) > self.attach_timeout:
                self.get_logger().warn("attach timeout/failed -> retry touch")
                self.attach_future = None
                self._set_state("TB3_TOUCH")
            return

        # 4) bring stone to arm zone
        if self.state == "TB3_GOTO_ARM":
            if self.go_to(self.arm_zone_xy, stop_dist=self.arm_stop_dist):
                self._set_state("DETACH")
            return

        # 5) detach (async). only after detach => arm
        if self.state == "DETACH":
            self.stop_hard(n=18, dt=0.02)
            self._start_detach()

            if self.detach_future is None:
                return

            if self.detach_future.done():
                res = None
                try:
                    res = self.detach_future.result()
                except Exception:
                    res = None
                self.detach_future = None

                ok = (res is not None and bool(res.ok))
                self.get_logger().info(f"DETACH done ok={ok}")

                if ok:
                    self.attached = False
                    self.stop_hard(n=16, dt=0.02)
                    # now arm may start
                    self._set_state("ARM_WORK")
                else:
                    # retry detach a bit
                    self.get_logger().warn("detach returned not ok -> retry detach")
                    self._set_state("DETACH")
                return

            if (time.time() - self.req_sent_t) > self.detach_timeout:
                self.get_logger().warn("detach timeout -> retry detach")
                self.detach_future = None
            return

        # 6) arm: only after detach success
        if self.state == "ARM_WORK":
            # TB3 must not move
            self.stop()

            if not self.arm_sent_once:
                self.arm_sent_once = True
                self.arm_started_t = time.time()
                self.send_arm_pick_place()
                self.get_logger().info("Arm trajectory sent (after DETACH).")

            # if you have a real gripper/IK, replace timing here
            if (time.time() - self.arm_started_t) > self.arm_total_time:
                self._set_state("DONE")
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

    # safe shutdown (avoid "context is invalid")
    try:
        if rclpy.ok():
            node.stop_hard(n=3, dt=0.01)
            node.stop()
    except Exception:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

