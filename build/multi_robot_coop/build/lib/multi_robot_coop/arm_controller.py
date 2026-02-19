import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')
        self.sub = self.create_subscription(Bool, '/task/arrived', self.cb, 10)
        self.pub = self.create_publisher(String, '/arm/symbolic_command', 10)
        self.done = False
        self.get_logger().info("Arm controller started. Waiting for /task/arrived...")

    def cb(self, msg: Bool):
        if msg.data and not self.done:
            self.get_logger().info("Received ARRIVED -> executing SYMBOLIC arm motion")
            self.pub.publish(String(data="ARM_MOVE_SYMBOLIC: pick/place sequence started"))
            self.done = True

def main():
    rclpy.init()
    node = ArmController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
