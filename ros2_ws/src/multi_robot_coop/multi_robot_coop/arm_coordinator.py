#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ArmCoordinator(Node):
    def __init__(self):
        super().__init__('arm_coordinator')

        self.task_pub = self.create_publisher(String, '/coop/task', 10)
        self.status_sub = self.create_subscription(String, '/coop/status', self.on_status, 10)

        self.sent = False
        self.timer = self.create_timer(1.0, self.on_timer)

        self.get_logger().info("ARM Coordinator ready.")

    def on_timer(self):
        if not self.sent:
            msg = String()
            msg.data = "scan_and_go"
            self.task_pub.publish(msg)
            self.get_logger().info("Sent task to TB3: scan_and_go")
            self.sent = True

    def on_status(self, msg: String):
        self.get_logger().info(f"Status from TB3: {msg.data}")
        if "arrived" in msg.data.lower():
            self.get_logger().info("ARM: received 'arrived'. (Here we would trigger arm action)")
            # اینجا می‌تونی بعداً فرمان واقعی بازو رو publish کنی

def main():
    rclpy.init()
    node = ArmCoordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
