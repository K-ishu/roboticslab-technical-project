#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')
        self.pub = self.create_publisher(String, '/arm_demo/state', 10)
        self.timer = self.create_timer(1.0, self.on_timer)
        self.step = 0
        self.get_logger().info("arm_controller started: publishing /arm_demo/state")

    def on_timer(self):
        # demo state machine (for architecture & presentation)
        states = ["IDLE", "MOVE_TO_PREGRASP", "GRASP", "LIFT", "PLACE", "RETURN_HOME"]
        msg = String()
        msg.data = states[self.step % len(states)]
        self.pub.publish(msg)
        self.get_logger().info(f"Arm demo state: {msg.data}")
        self.step += 1

def main():
    rclpy.init()
    node = ArmController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


