#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


JOINTS = [
    "lbr_iiwa_joint_1",
    "lbr_iiwa_joint_2",
    "lbr_iiwa_joint_3",
    "lbr_iiwa_joint_4",
    "lbr_iiwa_joint_5",
    "lbr_iiwa_joint_6",
    "lbr_iiwa_joint_7",
]


class ArmRealController(Node):
    """
    Controller that publishes JointTrajectory to ros2_control controller.
    - listens to /coop/task (String)
    - on command, publishes a sample trajectory to /iiwa_arm_controller/joint_trajectory
    """

    def __init__(self):
        super().__init__("arm_real_controller")

        self.traj_pub = self.create_publisher(
            JointTrajectory,
            "/iiwa_arm_controller/joint_trajectory",
            10
        )

        self.task_sub = self.create_subscription(
            String,
            "/coop/task",
            self.on_task,
            10
        )

        self.get_logger().info("ArmRealController ready. Waiting for /coop/task ...")

    def publish_pose(self, positions, secs=2):
        msg = JointTrajectory()
        msg.joint_names = JOINTS

        pt = JointTrajectoryPoint()
        pt.positions = [float(x) for x in positions]
        pt.time_from_start.sec = int(secs)
        pt.time_from_start.nanosec = 0

        msg.points = [pt]
        self.traj_pub.publish(msg)

    def on_task(self, msg: String):
        task = (msg.data or "").strip()
        self.get_logger().info(f"Received task: {task}")

        # چند حرکت نمونه
        if task in ("arm_test", "test_arm"):
            self.publish_pose([0.3, -0.6, 0.8, -0.4, 0.5, -0.3, 0.2], secs=2)
            self.get_logger().info("Published arm_test trajectory")

        elif task == "arm_home":
            self.publish_pose([0.0]*7, secs=2)
            self.get_logger().info("Published arm_home trajectory")

        # سناریوی تو: نزدیک ظرف/تگ‌بورد یک ژست ساده
        elif task == "place_near_target":
            self.publish_pose([-0.2, 0.4, 0.3, -0.6, 0.2, 0.3, 0.0], secs=3)
            self.get_logger().info("Published place_near_target trajectory")

        else:
            self.get_logger().warn("Unknown task. Try: arm_test | arm_home | place_near_target")


def main():
    rclpy.init()
    node = ArmRealController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

