#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MobileController(Node):
    def __init__(self):
        super().__init__('mobile_controller')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.on_timer)  # 10 Hz
        self.t = 0.0
        self.get_logger().info("mobile_controller started: publishing /cmd_vel")

    def on_timer(self):
        msg = Twist()
        # simple demo: drive forward for 5s, stop for 2s, rotate for 4s, repeat
        self.t += 0.1
        phase = self.t % 11.0

        if phase < 5.0:
            msg.linear.x = 0.2
            msg.angular.z = 0.0
        elif phase < 7.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.5

        self.pub.publish(msg)

def main():
    rclpy.init()
    node = MobileController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
