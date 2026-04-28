#!/usr/bin/env python3
import math
import time
import subprocess
from dataclasses import dataclass

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


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


@dataclass
class Pose2D:
    x: float
    y: float
    yaw: float


class ScenarioCoordinator(Node):
    def __init__(self):
        super().__init__("scenario_coordinator")

        # ===================== WORLD / COORDS =====================
        self.world_name = "lab_world"
        self.stone_name = "stone"

        self.stone_xy = (3.45662, -0.223026)
        self.arm_zone_center = (-1.05, -0.55)
        self.container_xy = (-1.54015, -1.08473)

        # ===================== WAYPOINTS (KEEP THIS) =====================
        self.waypoints = [
            (1.20, -3.90),
            (2.60, -3.20),
            (3.90, -1.80),
        ]
        self.wp_idx = 0

        # ===================== TOPICS =====================
        self.cmd_vel_topic = "/cmd_vel"
        self.scan_topic = "/tb3/scan"
        self.odom_topic = "/odom"
        self.traj_topic = "/iiwa_arm_controller/joint_trajectory"
        self.status_topic = "/scenario_status"

        self.pub_cmd = self.create_publisher(Twist, self.cmd_vel_topic, 10)
        self.pub_traj = self.create_publisher(JointTrajectory, self.traj_topic, 10)
        self.pub_status = self.create_publisher(String, self.status_topic, 10)

        self.sub_odom = self.create_subscription(Odometry, self.odom_topic, self.cb_odom, 10)
        self.sub_scan = self.create_subscription(LaserScan, self.scan_topic, self.cb_scan, 10)

        # ===================== STATE =====================
        self.tb3_pose: Pose2D | None = None
        self.scan: LaserScan | None = None

        self.state = "INIT"
        self.state_t0 = time.time()

        self.attached = False

        # ===================== TUNING =====================
        self.behind_dist = 0.95            # پشت سنگ (دورتر)
        self.pre_attach_dist = 0.55        # پشت سنگ (نزدیک‌تر) برای اینکه دقیقاً از پشت بیاد
        self.attach_offset = 0.22          # سنگ جلوی ربات وقتی attach است
        self.detach_dist_to_arm = 0.75

        self.v_go = 0.20
        self.v_approach = 0.12            # نزدیک شدن مستقیم به سنگ
        self.v_push = 0.18
        self.w_max = 1.1

        self.stop_d = 0.30
        self.slow_d = 0.52

        # stuck detector (فقط حرکت جلو)
        self._last_stuck_check_t = time.time()
        self._last_stuck_pose = None
        self._last_cmd = Twist()

        self.timer = self.create_timer(0.05, self.loop)
        self.get_logger().info("ScenarioCoordinator started.")
        self.publish_status("INIT")

    # ---------------- callbacks ----------------
    def cb_odom(self, msg: Odometry):
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        yaw = yaw_from_quat(q.x, q.y, q.z, q.w)
        self.tb3_pose = Pose2D(p.x, p.y, yaw)

    def cb_scan(self, msg: LaserScan):
        self.scan = msg

    # ---------------- basic helpers ----------------
    def publish_status(self, s: str):
        m = String()
        m.data = s
        self.pub_status.publish(m)
        self.get_logger().info(f"STATUS: {s}")

    def set_state(self, s: str):
        self.state = s
        self.state_t0 = time.time()
        self.publish_status(s)

    def elapsed(self):
        return time.time() - self.state_t0

    def stop_tb3(self):
        t = Twist()
        self.pub_cmd.publish(t)
        self._last_cmd = t

    def drive_tb3(self, lin, ang):
        t = Twist()
        t.linear.x = float(lin)
        t.angular.z = float(ang)
        self.pub_cmd.publish(t)
        self._last_cmd = t

    def angle_diff(self, a, b):
        return wrap_to_pi(a - b)

    def dist_to_xy(self, xy):
        if self.tb3_pose is None:
            return 1e9
        return math.hypot(self.tb3_pose.x - xy[0], self.tb3_pose.y - xy[1])

    def unit_from_to(self, a_xy, b_xy):
        dx = b_xy[0] - a_xy[0]
        dy = b_xy[1] - a_xy[1]
        d = math.hypot(dx, dy)
        if d < 1e-6:
            return (1.0, 0.0)
        return (dx / d, dy / d)

    def push_heading_world(self):
        ux, uy = self.unit_from_to(self.stone_xy, self.arm_zone_center)
        return math.atan2(uy, ux)

    def behind_point(self, dist):
        ux, uy = self.unit_from_to(self.stone_xy, self.arm_zone_center)
        return (self.stone_xy[0] - ux * dist, self.stone_xy[1] - uy * dist)

    # ---------------- LiDAR windows ----------------
    def scan_min_in_window(self, center_rad, half_width_rad):
        if self.scan is None:
            return float("inf")
        msg = self.scan
        best = float("inf")
        ang = msg.angle_min
        for r in msg.ranges:
            if math.isfinite(r) and msg.range_min < r < msg.range_max:
                a = wrap_to_pi(ang)
                if abs(wrap_to_pi(a - center_rad)) <= half_width_rad:
                    best = min(best, r)
            ang += msg.angle_increment
        return best

    def front_clear(self):
        # برای نزدیک شدن مستقیم، فقط جلوی ربات مهمه
        return self.scan_min_in_window(0.0, math.radians(15))

    # ---------------- Avoidance ----------------
    def compute_avoidance(self, desired_lin, desired_ang):
        front = self.scan_min_in_window(0.0, math.radians(20))
        left = self.scan_min_in_window(+math.radians(60), math.radians(20))
        right = self.scan_min_in_window(-math.radians(60), math.radians(20))

        lin = desired_lin
        ang = desired_ang

        if front < self.stop_d:
            lin = 0.0
            ang = +0.9 if left > right else -0.9
            return lin, ang

        if front < self.slow_d:
            lin = min(lin, 0.10)

        side_push = 0.0
        if left < 0.62:
            side_push -= (0.62 - left) * 0.8
        if right < 0.62:
            side_push += (0.62 - right) * 0.8

        ang = clamp(ang + side_push, -1.2, 1.2)
        lin = clamp(lin, 0.0, 0.24)
        return lin, ang

    def goto_xy_avoid(self, goal_xy, stop_dist=0.6, v=0.20):
        if self.tb3_pose is None:
            return False

        gx, gy = goal_xy
        dx = gx - self.tb3_pose.x
        dy = gy - self.tb3_pose.y
        dist = math.hypot(dx, dy)

        if dist < stop_dist:
            self.stop_tb3()
            return True

        target_yaw = math.atan2(dy, dx)
        yaw_err = self.angle_diff(target_yaw, self.tb3_pose.yaw)

        desired_ang = clamp(1.2 * yaw_err, -self.w_max, self.w_max)
        desired_lin = v * (1.0 - min(1.0, abs(yaw_err)))
        desired_lin = max(0.07, desired_lin)

        lin, ang = self.compute_avoidance(desired_lin, desired_ang)
        self.drive_tb3(lin, ang)
        return False

    def face_yaw(self, target_yaw, tol_deg=6):
        if self.tb3_pose is None:
            return False
        err = self.angle_diff(target_yaw, self.tb3_pose.yaw)
        if abs(err) < math.radians(tol_deg):
            self.stop_tb3()
            return True
        lin, ang = self.compute_avoidance(0.0, clamp(1.3 * err, -0.85, 0.85))
        self.drive_tb3(lin, ang)
        return False

    # ---------------- stuck ----------------
    def is_stuck_forward_only(self):
        if self.tb3_pose is None:
            return False

        now = time.time()
        if now - self._last_stuck_check_t < 3.0:
            return False

        if self._last_stuck_pose is None:
            self._last_stuck_pose = (self.tb3_pose.x, self.tb3_pose.y)
            self._last_stuck_check_t = now
            return False

        moved = math.hypot(self.tb3_pose.x - self._last_stuck_pose[0], self.tb3_pose.y - self._last_stuck_pose[1])
        self._last_stuck_pose = (self.tb3_pose.x, self.tb3_pose.y)
        self._last_stuck_check_t = now

        cmd_forward = self._last_cmd.linear.x > 0.08
        return cmd_forward and moved < 0.03

    # ---------------- gazebo pose modify (attach/detach) ----------------
    def gz_set_model_pose(self, model_name: str, x: float, y: float, z: float, yaw: float = 0.0):
        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)

        topic = f"/gazebo/{self.world_name}/pose/modify"
        msg = (
            f"name: '{model_name}' "
            f"position {{ x: {x} y: {y} z: {z} }} "
            f"orientation {{ x: 0 y: 0 z: {qz} w: {qw} }}"
        )
        cmd = ["gz", "topic", "-t", topic, "-m", "gazebo.msgs.Pose", "-p", msg]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            self.get_logger().error(f"gz_set_model_pose failed: {e}")
            return False

    def attach_update(self):
        if not self.attached or self.tb3_pose is None:
            return
        x = self.tb3_pose.x + math.cos(self.tb3_pose.yaw) * self.attach_offset
        y = self.tb3_pose.y + math.sin(self.tb3_pose.yaw) * self.attach_offset
        self.gz_set_model_pose(self.stone_name, x, y, 0.125, yaw=0.0)

    def do_attach(self):
        self.attached = True
        # همون لحظه سنگ رو snap کن جلوی ربات (خیلی مهم)
        self.attach_update()
        self.get_logger().info("STONE ATTACHED (magnetic/vacuum)")

    def do_detach(self):
        self.attached = False
        self.get_logger().info("STONE DETACHED")

    # ---------------- arm trajectory ----------------
    def send_arm_trajectory(self):
        jt = JointTrajectory()
        jt.joint_names = [
            "lbr_iiwa_joint_1",
            "lbr_iiwa_joint_2",
            "lbr_iiwa_joint_3",
            "lbr_iiwa_joint_4",
            "lbr_iiwa_joint_5",
            "lbr_iiwa_joint_6",
            "lbr_iiwa_joint_7",
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
        done      = home

        jt.points = [
            pt(home, 2),
            pt(pre_pick, 5),
            pt(lift, 8),
            pt(pre_place, 12),
            pt(done, 15),
        ]
        self.pub_traj.publish(jt)

    # ---------------- recovery ----------------
    def recovery_action(self):
        t = self.elapsed()
        if t < 0.8:
            self.drive_tb3(-0.10, 0.0)
            return
        if t < 2.0:
            self.drive_tb3(0.0, 0.85)
            return
        if t < 2.6:
            self.drive_tb3(+0.08, 0.0)
            return
        self.stop_tb3()
        self.set_state("TB3_GOTO_WAYPOINTS")

    # ---------------- approach stone straight (key fix) ----------------
    def approach_stone_from_behind(self):
        """
        فقط مستقیم از پشت به سمت سنگ برو.
        - heading قفل روی push_heading
        - اگر جلوی ربات خیلی نزدیک شد stop/recover
        - وقتی dist به سنگ < 0.45 -> موفق
        """
        if self.tb3_pose is None:
            return False

        # قفل جهت روی push_heading (یعنی از پشت به سمت سنگ/بازو)
        target_yaw = self.push_heading_world()
        yaw_err = wrap_to_pi(target_yaw - self.tb3_pose.yaw)
        ang = clamp(1.1 * yaw_err, -0.7, 0.7)

        # امنیت جلو
        front = self.front_clear()
        if front < 0.28:
            self.stop_tb3()
            return False

        # نزدیک شدن
        if self.dist_to_xy(self.stone_xy) < 0.45:
            self.stop_tb3()
            return True

        # اینجا Avoidance جانبی رو کمتر کن که از بغل فرار نکنه
        # فقط اگر خیلی نزدیک مانع بود، کم کن
        lin = self.v_approach
        if front < 0.50:
            lin = 0.08

        self.drive_tb3(lin, ang)
        return False

    # ---------------- main loop ----------------
    def loop(self):
        if self.tb3_pose is None:
            return

        self.attach_update()

        if self.state in ("TB3_GOTO_WAYPOINTS", "TB3_GOTO_BEHIND_STONE", "TB3_GOTO_PRE_ATTACH", "TB3_PUSHING_TO_ARM"):
            if self.is_stuck_forward_only():
                self.get_logger().warn("TB3 seems stuck -> recovery")
                self.set_state("TB3_RECOVERY")
                return

        if self.state == "INIT":
            self.attached = False
            self.wp_idx = 0
            self._last_stuck_pose = (self.tb3_pose.x, self.tb3_pose.y)
            self._last_stuck_check_t = time.time()
            self.set_state("TB3_GOTO_WAYPOINTS")
            return

        if self.state == "TB3_RECOVERY":
            self.recovery_action()
            return

        # 0) WAYPOINTS (KEEP)
        if self.state == "TB3_GOTO_WAYPOINTS":
            if self.wp_idx >= len(self.waypoints):
                self.set_state("TB3_GOTO_BEHIND_STONE")
                return

            wp = self.waypoints[self.wp_idx]
            done = self.goto_xy_avoid(wp, stop_dist=0.55, v=self.v_go)
            if done:
                self.wp_idx += 1
            if self.elapsed() > 120.0:
                self.set_state("TB3_RECOVERY")
            return

        # 1) پشت سنگ (دورتر)
        if self.state == "TB3_GOTO_BEHIND_STONE":
            behind = self.behind_point(self.behind_dist)
            done = self.goto_xy_avoid(behind, stop_dist=0.65, v=self.v_go)
            if done:
                self.set_state("TB3_GOTO_PRE_ATTACH")
                return
            if self.elapsed() > 90.0:
                self.set_state("TB3_RECOVERY")
            return

        # 1.5) پشت سنگ (نزدیک‌تر) -> جلوی «از بغل رد شدن» را می‌گیرد
        if self.state == "TB3_GOTO_PRE_ATTACH":
            pre = self.behind_point(self.pre_attach_dist)
            done = self.goto_xy_avoid(pre, stop_dist=0.45, v=0.16)
            if done:
                self.set_state("TB3_FACE_STONE_PUSH_DIR")
                return
            if self.elapsed() > 60.0:
                self.set_state("TB3_RECOVERY")
            return

        # 2) رو به جهت push
        if self.state == "TB3_FACE_STONE_PUSH_DIR":
            if self.face_yaw(self.push_heading_world(), tol_deg=5):
                self.set_state("TB3_APPROACH_STONE_STRAIGHT")
            if self.elapsed() > 35.0:
                self.set_state("TB3_RECOVERY")
            return

        # 3) ✅ نزدیک شدن مستقیم از پشت تا سنگ دقیقاً جلوی ربات بیاد
        if self.state == "TB3_APPROACH_STONE_STRAIGHT":
            ok = self.approach_stone_from_behind()
            if ok:
                self.set_state("TB3_ATTACH_STONE")
                return
            if self.elapsed() > 35.0:
                self.set_state("TB3_RECOVERY")
            return

        # 4) Attach قطعی
        if self.state == "TB3_ATTACH_STONE":
            self.do_attach()
            self.set_state("TB3_PUSHING_TO_ARM")
            return

        # 5) بردن سنگ به سمت بازو
        if self.state == "TB3_PUSHING_TO_ARM":
            d_to_arm = self.dist_to_xy(self.arm_zone_center)
            if d_to_arm < self.detach_dist_to_arm:
                self.stop_tb3()
                self.set_state("TB3_DETACH_NEAR_ARM")
                return

            gx, gy = self.arm_zone_center
            dx = gx - self.tb3_pose.x
            dy = gy - self.tb3_pose.y
            goal_yaw = math.atan2(dy, dx)
            yaw_err = wrap_to_pi(goal_yaw - self.tb3_pose.yaw)

            desired_ang = clamp(1.0 * yaw_err, -1.0, 1.0)
            lin, ang = self.compute_avoidance(self.v_push, desired_ang)
            self.drive_tb3(min(lin, 0.20), ang)

            if self.elapsed() > 140.0:
                self.set_state("TB3_RECOVERY")
            return

        # 6) detach نزدیک بازو + شروع بازو
        if self.state == "TB3_DETACH_NEAR_ARM":
            px, py = self.arm_zone_center
            self.gz_set_model_pose(self.stone_name, px, py, 0.125, yaw=0.0)
            self.do_detach()
            self.set_state("STONE_AT_ARM_ZONE")
            return

        if self.state == "STONE_AT_ARM_ZONE":
            self.stop_tb3()
            self.send_arm_trajectory()
            self.set_state("ARM_WORKING")
            return

        if self.state == "ARM_WORKING":
            t = self.elapsed()
            if 7.5 < t < 8.5:
                self.gz_set_model_pose(self.stone_name, self.container_xy[0], self.container_xy[1], 0.30, yaw=0.0)
            if 11.5 < t < 12.5:
                self.gz_set_model_pose(self.stone_name, self.container_xy[0], self.container_xy[1], 0.08, yaw=0.0)
            if t > 16.5:
                self.set_state("ARM_DONE")
            return

        if self.state == "ARM_DONE":
            self.stop_tb3()
            return


def main():
    rclpy.init()
    node = ScenarioCoordinator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.stop_tb3()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

