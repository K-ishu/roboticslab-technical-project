#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class TB3Coordinator(Node):
    def __init__(self):
        super().__init__('tb3_coordinator')

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_pub = self.create_publisher(String, '/coop/status', 10)
        self.task_sub = self.create_subscription(String, '/coop/task', self.on_task, 10)

        self.timer = self.create_timer(0.2, self.on_timer)  # 5Hz
        self.active = False
        self.ticks_left = 0

        self.get_logger().info("TB3 Coordinator ready. Waiting for /coop/task ...")

    def on_task(self, msg: String):
        self.get_logger().info(f"Received task: {msg.data}")
        if msg.data.strip().lower() == 'scan_and_go':
            # حرکت نمادین: 4 ثانیه جلو برو
            self.active = True
            self.ticks_left = int(4.0 / 0.2)
            st = String()
            st.data = "TB3: starting symbolic motion (forward 4s)"
            self.status_pub.publish(st)

    def on_timer(self):
        if self.active and self.ticks_left > 0:
            tw = Twist()
            tw.linear.x = 0.15
            self.cmd_pub.publish(tw)
            self.ticks_left -= 1
            if self.ticks_left == 0:
                self.active = False
                self.cmd_pub.publish(Twist())  # stop
                st = String()
                st.data = "TB3: symbolic motion done. Sending 'arrived' status."
                self.status_pub.publish(st)
                self.get_logger().info("Symbolic motion done.")

def main():
    rclpy.init()
    node = TB3Coordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
