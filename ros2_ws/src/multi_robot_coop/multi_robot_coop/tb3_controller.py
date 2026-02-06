import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class TB3Controller(Node):
    def __init__(self):
        super().__init__('tb3_controller')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.arrived_pub = self.create_publisher(Bool, '/task/arrived', 10)

        self.start_time = time.time()
        self.duration = 6.0   # seconds of motion (adjust if needed)
        self.timer = self.create_timer(0.1, self.loop)

        self.sent_arrived = False
        self.get_logger().info("TB3 controller started. Publishing /cmd_vel then /task/arrived")

    def loop(self):
        t = time.time() - self.start_time
        msg = Twist()

        if t < self.duration:
            msg.linear.x = 0.15
            msg.angular.z = 0.0
            self.cmd_pub.publish(msg)
        else:
            # stop
            self.cmd_pub.publish(Twist())

            if not self.sent_arrived:
                self.arrived_pub.publish(Bool(data=True))
                self.get_logger().info("ARRIVED -> published /task/arrived = True")
                self.sent_arrived = True

def main():
    rclpy.init()
    node = TB3Controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
