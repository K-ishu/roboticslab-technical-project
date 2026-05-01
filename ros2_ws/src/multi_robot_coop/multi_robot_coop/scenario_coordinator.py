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


class ScenarioCoordinator(Node):
    def __init__(self):
        super().__init__("scenario_coordinator")

        self.odom_topic = self.declare_parameter("odom_topic", "/odom").value
        self.scan_topic = self.declare_parameter("scan_topic", "/tb3/scan").value
        self.cmd_vel_topic = self.declare_parameter("cmd_vel_topic", "/cmd_vel").value

        self.attach_service = self.declare_parameter("attach_service", "/attach").value
        self.detach_service = self.declare_parameter("detach_service", "/detach").value

        self.tb3_model = self.declare_parameter("tb3_model", "tb3").value
        self.tb3_link = self.declare_parameter("tb3_link", "base_link").value

        self.stone_model = self.declare_parameter("stone_model", "stone").value
        self.stone_link = self.declare_parameter("stone_link", "stone_link").value

        self.arm_model = self.declare_parameter("arm_model", "lbr_iiwa").value
        self.arm_ee_link = self.declare_parameter("arm_ee_link", "lbr_iiwa_tool").value
        self.arm_stone_link = self.declare_parameter("arm_stone_link", "stone_grasp_link").value

        stone_xy = self.declare_parameter("stone_xy", [3.45662, -0.223026]).value
        arm_xy = self.declare_parameter("arm_xy", [-1.3, -0.3]).value
        start_xy = self.declare_parameter("start_xy", [1.05255, -4.70317]).value
        push_xy = self.declare_parameter("push_xy", [-0.75, -0.30]).value

        self.stone_xy = (float(stone_xy[0]), float(stone_xy[1]))
        self.arm_xy = (float(arm_xy[0]), float(arm_xy[1]))
        self.start_xy = (float(start_xy[0]), float(start_xy[1]))
        self.push_xy = (float(push_xy[0]), float(push_xy[1]))

        self.place_xy = (-1.54015, -1.08473)

        self.v_nav = float(self.declare_parameter("v_nav", 0.22).value)
        self.v_touch = float(self.declare_parameter("v_touch", 0.05).value)
        self.v_push = float(self.declare_parameter("v_push", 0.10).value)

        self.w_fast = float(self.declare_parameter("w_fast", 0.9).value)
        self.w_align = float(self.declare_parameter("w_align", 0.45).value)

        self.goto_stone_area_dist = float(self.declare_parameter("goto_stone_area_dist", 0.95).value)
        self.push_goal_dist = float(self.declare_parameter("push_goal_dist", 0.18).value)

        self.attach_dist = float(self.declare_parameter("attach_dist", 0.18).value)
        self.attach_angle_deg = float(self.declare_parameter("attach_angle_deg", 8.0).value)

        self.attached_ignore_front_deg = float(self.declare_parameter("attached_ignore_front_deg", 35.0).value)
        self.attached_ignore_front_dist = float(self.declare_parameter("attached_ignore_front_dist", 0.32).value)

        self.search_timeout = float(self.declare_parameter("search_timeout", 20.0).value)
        self.push_timeout = float(self.declare_parameter("push_timeout", 55.0).value)
        self.service_timeout = float(self.declare_parameter("service_timeout", 5.0).value)

        self.pub_cmd = self.create_publisher(Twist, self.cmd_vel_topic, 10)
        self.pub_status = self.create_publisher(String, "/scenario_status", 10)
        self.pub_traj = self.create_publisher(
            JointTrajectory,
            "/iiwa_arm_controller/joint_trajectory",
            10,
        )

        self.create_subscription(Odometry, self.odom_topic, self.cb_odom, 10)
        self.create_subscription(LaserScan, self.scan_topic, self.cb_scan, 10)

        self.cli_attach = self.create_client(Attach, self.attach_service)
        self.cli_detach = self.create_client(Attach, self.detach_service)

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

        self.arm_started = False
        self.arm_attach_sent = False
        self.arm_detach_sent = False

        self.timer = self.create_timer(0.05, self.loop)
        self.get_logger().info("Scenario Coordinator Started")

    def cb_odom(self, msg: Odometry):
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        self.x = p.x
        self.y = p.y
        self.yaw = yaw_from_quat(q.x, q.y, q.z, q.w)

    def cb_scan(self, msg: LaserScan):
        self.scan = msg

    def set_state(self, s):
        self.state = s
        self.state_t0 = time.time()
        m = String()
        m.data = s
        self.pub_status.publish(m)
        self.get_logger().info(f"STATE {s}")

    def elapsed(self):
        return time.time() - self.state_t0

    def stop(self):
        self.pub_cmd.publish(Twist())

    def stop_hard(self, n=8, dt=0.02):
        t = Twist()
        for _ in range(n):
            self.pub_cmd.publish(t)
            time.sleep(dt)

    def drive(self, v, w):
        t = Twist()
        t.linear.x = float(v)
        t.angular.z = float(w)
        self.pub_cmd.publish(t)

    def dist_to(self, xy):
        return math.hypot(xy[0] - self.x, xy[1] - self.y)

    def angle_to(self, xy):
        return wrap_to_pi(math.atan2(xy[1] - self.y, xy[0] - self.x) - self.yaw)

    def scan_objects(self, ignore_attached=False):
        if self.scan is None:
            return None, float("inf"), float("inf")

        front_best = None
        left_min = float("inf")
        right_min = float("inf")

        ang = self.scan.angle_min
        for r in self.scan.ranges:
            if math.isfinite(r) and self.scan.range_min < r < self.scan.range_max:
                a = wrap_to_pi(ang)
                deg = math.degrees(a)

                if ignore_attached:
                    if abs(deg) <= self.attached_ignore_front_deg and r <= self.attached_ignore_front_dist:
                        ang += self.scan.angle_increment
                        continue

                if abs(deg) <= 35.0:
                    if front_best is None or r < front_best[0]:
                        front_best = (r, a)

                if 20.0 <= deg <= 80.0:
                    left_min = min(left_min, r)

                if -80.0 <= deg <= -20.0:
                    right_min = min(right_min, r)

            ang += self.scan.angle_increment

        return front_best, left_min, right_min

    def nav_to_point(self, goal_xy, stop_dist=0.4, v_nom=0.22):
        d = self.dist_to(goal_xy)
        if d <= stop_dist:
            self.stop_hard()
            return True

        err = self.angle_to(goal_xy)
        front_obj, left_min, right_min = self.scan_objects(ignore_attached=self.attached)
        front_r = front_obj[0] if front_obj is not None else 999.0

        if front_r < 0.22:
            turn = -self.w_fast if left_min < right_min else self.w_fast
            self.drive(0.0, turn)
            return False

        avoid = 0.0
        if left_min < 0.40:
            avoid -= 0.7
        if right_min < 0.40:
            avoid += 0.7

        w = clamp(1.3 * err + avoid, -self.w_fast, self.w_fast)
        v = v_nom * max(0.20, 1.0 - min(abs(err) / 1.4, 0.85))

        if front_r < 0.35:
            v = min(v, 0.05)
        elif front_r < 0.55:
            v = min(v, 0.10)

        self.drive(v, w)
        return False

    def stone_front_obj(self):
        if self.scan is None:
            return None

        best = None
        ang = self.scan.angle_min

        for r in self.scan.ranges:
            if math.isfinite(r) and self.scan.range_min < r < self.scan.range_max:
                a = wrap_to_pi(ang)
                if abs(math.degrees(a)) <= 25.0:
                    if best is None or r < best[0]:
                        best = (r, a)
            ang += self.scan.angle_increment

        return best

    def make_tb3_stone_req(self):
        req = Attach.Request()
        req.model_name_1 = self.tb3_model
        req.link_name_1 = self.tb3_link
        req.model_name_2 = self.stone_model
        req.link_name_2 = self.stone_link
        return req

    def make_arm_stone_req(self):
        req = Attach.Request()
        req.model_name_1 = self.arm_model
        req.link_name_1 = self.arm_ee_link
        req.model_name_2 = self.stone_model
        req.link_name_2 = self.arm_stone_link
        return req

    def gz_set_model_pose(self, model_name, x, y, z, yaw=0.0):
        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)

        cmd = [
            "gz", "topic",
            "-t", "/gazebo/lab_world/pose/modify",
            "-m", "gazebo.msgs.Pose",
            "-p",
            f"name: '{model_name}' "
            f"position {{ x: {x} y: {y} z: {z} }} "
            f"orientation {{ x: 0 y: 0 z: {qz} w: {qw} }}",
        ]

        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except Exception:
            pass

    def send_arm_pick_place(self):
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

        home = [0.0, 0.4, 0.0, -1.2, 0.0, 1.0, 0.0]
        pre_pick = [0.2, 0.9, 0.0, -1.7, 0.0, 1.2, 0.0]
        lift = [0.2, 0.3, 0.0, -1.1, 0.0, 1.0, 0.0]

        pre_place = [-1.90, 1.05, 0.0, -1.25, 0.0, 1.10, 0.0]
        place = [-1.93, 0.98, 0.0, -1.35, 0.0, 1.05, 0.0]

        back_home = [0.0, 0.4, 0.0, -1.2, 0.0, 1.0, 0.0]

        jt.points = [
            pt(home, 2),
            pt(pre_pick, 6),
            pt(lift, 12),
            pt(pre_place, 35),
            pt(place, 48),
            pt(back_home, 62),
        ]

        self.pub_traj.publish(jt)

    def stuck_recovery(self):
        t = self.elapsed()
        if t < 0.8:
            self.drive(-0.10, 0.0)
        elif t < 1.8:
            self.drive(0.0, 0.8)
        elif t < 2.7:
            self.drive(0.10, 0.0)
        else:
            self.stop_hard()
            if self.attached:
                self.set_state("PUSH_TO_ARM")
            else:
                self.set_state("STONE_SEARCH")

    def loop(self):
        if self.x is None or self.scan is None:
            return

        if self.state == "INIT":
            self.set_state("GOTO_STONE_AREA")
            return

        if self.state == "GOTO_STONE_AREA":
            done = self.nav_to_point(
                self.stone_xy,
                stop_dist=self.goto_stone_area_dist,
                v_nom=self.v_nav,
            )
            self.get_logger().info(f"STATE GOTO_STONE pose=({self.x:.2f},{self.y:.2f})")

            if done:
                self.stop_hard()
                self.set_state("STONE_SEARCH")
            return

        if self.state == "STONE_SEARCH":
            if self.elapsed() > self.search_timeout:
                self.stop_hard()
                self.set_state("GOTO_STONE_AREA")
                return

            obj = self.stone_front_obj()
            if obj is None:
                self.drive(0.0, 0.35)
                return

            self.stop_hard()
            self.set_state("STONE_ALIGN")
            return

        if self.state == "STONE_ALIGN":
            obj = self.stone_front_obj()
            self.get_logger().info(f"STATE STONE_ALIGN pose=({self.x:.2f},{self.y:.2f})")

            if obj is None:
                self.set_state("STONE_SEARCH")
                return

            r, a = obj
            a_deg = math.degrees(a)

            if r <= self.attach_dist and abs(a_deg) <= self.attach_angle_deg:
                self.stop_hard()
                self.set_state("ATTACH_TB3")
                return

            if abs(a_deg) > 6.0:
                self.drive(0.0, clamp(1.5 * a, -self.w_align, self.w_align))
                return

            if r > self.attach_dist:
                self.drive(self.v_touch, clamp(0.8 * a, -0.25, 0.25))
                return

            self.set_state("ATTACH_TB3")
            return

        if self.state == "ATTACH_TB3":
            self.stop_hard()

            if self.attach_future is None:
                if not self.cli_attach.service_is_ready():
                    self.get_logger().warn("attach service not ready yet...")
                    return

                self.attach_future = self.cli_attach.call_async(self.make_tb3_stone_req())
                self.req_sent_t = time.time()
                self.get_logger().info("Attach request sent (async).")
                return

            if self.attach_future.done():
                res = self.attach_future.result()
                self.attach_future = None

                if res is not None and res.ok:
                    self.attached = True
                    self.get_logger().info("TB3 ATTACH OK")
                    self.set_state("PUSH_TO_ARM")
                else:
                    self.get_logger().warn("TB3 attach failed -> back to STONE_ALIGN")
                    self.set_state("STONE_ALIGN")
                return

            if time.time() - self.req_sent_t > self.service_timeout:
                self.get_logger().warn("attach future timeout")
                self.attach_future = None
                self.set_state("STONE_ALIGN")
            return

        if self.state == "PUSH_TO_ARM":
            if self.elapsed() > self.push_timeout:
                self.get_logger().warn("push timeout -> go detach anyway")
                self.set_state("DETACH_TB3")
                return

            done = self.nav_to_point(
                self.push_xy,
                stop_dist=self.push_goal_dist,
                v_nom=self.v_push,
            )
            self.get_logger().info(f"PUSH_TO_ARM pose=({self.x:.2f},{self.y:.2f})")

            obj, _, _ = self.scan_objects(ignore_attached=True)
            front_r = obj[0] if obj is not None else 999.0

            if front_r < 0.18:
                self.get_logger().warn("Front blocked during push -> small escape")
                self.set_state("RECOVERY")
                return

            if done:
                self.stop_hard()
                self.set_state("DETACH_TB3")
            return

        if self.state == "DETACH_TB3":
            self.stop_hard()

            if self.detach_future is None:
                if not self.cli_detach.service_is_ready():
                    self.get_logger().warn("detach service not ready yet...")
                    return

                self.detach_future = self.cli_detach.call_async(self.make_tb3_stone_req())
                self.req_sent_t = time.time()
                self.get_logger().info("Detach request sent (async).")
                return

            if self.detach_future.done():
                res = self.detach_future.result()
                self.detach_future = None

                if res is not None and res.ok:
                    self.attached = False
                    self.get_logger().info("DETACH DONE")
                    self.set_state("ARM_PICK_PLACE")
                else:
                    self.get_logger().warn("detach failed -> retry")
                return

            if time.time() - self.req_sent_t > self.service_timeout:
                self.get_logger().warn("detach timeout -> retry")
                self.detach_future = None
            return

        if self.state == "ARM_PICK_PLACE":
            self.stop()

            if not self.arm_started:
                self.gz_set_model_pose(self.stone_model, -1.08, -0.30, 0.04, 0.0)
                time.sleep(1.5)

                for _ in range(5):
                    self.send_arm_pick_place()
                    time.sleep(0.05)

                self.arm_started = True
                self.arm_attach_sent = False
                self.arm_detach_sent = False
                self.state_t0 = time.time()
                self.get_logger().info("Arm trajectory published for REAL attach.")
                return

            t = self.elapsed()

            if 6.8 < t < 7.6 and not self.arm_attach_sent:
                self.gz_set_model_pose(self.stone_model, -1.08, -0.30, 0.04, 0.0)
                return

            if t >= 7.6 and not self.arm_attach_sent:
                if self.cli_attach.service_is_ready():
                    time.sleep(0.5)
                    self.cli_attach.call_async(self.make_arm_stone_req())
                    self.arm_attach_sent = True
                    self.get_logger().info("ARM_GRASP OK - real attach")
                return

            if t >= 56.0 and not self.arm_detach_sent:
                if self.cli_detach.service_is_ready():
                    time.sleep(0.5)
                    self.cli_detach.call_async(self.make_arm_stone_req())
                    self.arm_detach_sent = True
                    self.get_logger().info("ARM_RELEASE OK - real detach")
                return

            if 56.2 < t < 62.0 and self.arm_detach_sent:
                self.gz_set_model_pose(self.stone_model, -1.54015, -1.08473, 0.24, 0.0)
                return

            if t > 62.0:
                self.set_state("RETURN_HOME")
                return

        if self.state == "RETURN_HOME":
            done = self.nav_to_point(self.start_xy, stop_dist=0.15, v_nom=0.15)
            if done:
                self.stop_hard()
                self.set_state("DONE")
            return

        if self.state == "RECOVERY":
            self.get_logger().warn("Recovery mode")
            self.stuck_recovery()
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
        node.stop_hard()
        node.stop()
    except Exception:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
