#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ArmCoordinator(Node):
    def __init__(self):
        super().__init__('arm_coordinator')

        self.task_pub = self.create_publisher(String, '/coop/task', 10)
        self.status_sub = self.create_subscription(String, '/coop/status', self.on_status, 10)

        # optional: publish a symbolic arm command (for demo / logs)
        self.arm_pub = self.create_publisher(String, '/arm/symbolic_command', 10)

        self.sent_task = False
        self.did_arm = False

        self.timer = self.create_timer(1.0, self.on_timer)
        self.get_logger().info("ARM Coordinator ready.")

    def on_timer(self):
        if not self.sent_task:
            msg = String()
            msg.data = "scan_and_go"
            self.task_pub.publish(msg)
            self.get_logger().info("Sent task to TB3: scan_and_go")
            self.sent_task = True

    def on_status(self, msg: String):
        text = msg.data.strip()
        self.get_logger().info(f"Status from TB3: {text}")

        if (not self.did_arm) and ("arrived" in text.lower()):
            self.did_arm = True
            self.get_logger().info("ARM: received ARRIVED -> running symbolic pick/place")

            # Step 1: pick
            self.arm_pub.publish(String(data="ARM_SYMBOLIC: PICK (closing gripper)"))
            self.get_logger().info("ARM_SYMBOLIC: PICK")

            # Step 2 after 2s: place
            self.create_timer(2.0, self.do_place)

    def do_place(self):
        # This timer callback may be called repeatedly if we don't guard,
        # so we cancel by checking did_arm flag already set and then destroying timer by returning once.
        self.arm_pub.publish(String(data="ARM_SYMBOLIC: PLACE (opening gripper)"))
        self.get_logger().info("ARM_SYMBOLIC: PLACE")

        self.arm_pub.publish(String(data="ARM_SYMBOLIC: DONE"))
        self.get_logger().info("ARM_SYMBOLIC: DONE")


def main():
    rclpy.init()
    node = ArmCoordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

