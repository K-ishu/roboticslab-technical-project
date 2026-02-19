#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


class TB3Coordinator(Node):
    def __init__(self):
        super().__init__('tb3_coordinator')

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_pub = self.create_publisher(String, '/coop/status', 10)
        self.task_sub = self.create_subscription(String, '/coop/task', self.on_task, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.on_scan, 10)

        self.dt = 0.2
        self.timer = self.create_timer(self.dt, self.on_timer)

        self.state = "IDLE"   # IDLE / ROTATE / GO
        self.ticks_left = 0

        self.rotate_time = 2.0
        self.go_time = 4.0

        self.blocked = False
        self.safe_dist = 0.45
        self.front_angle_deg = 20.0

        self.fwd_speed = 0.15
        self.turn_speed = 0.6

        self.get_logger().info("TB3 Coordinator ready. Waiting for /coop/task ...")

    def publish_status(self, text: str):
        self.status_pub.publish(String(data=text))

    def on_task(self, msg: String):
        task = msg.data.strip().lower()
        self.get_logger().info(f"Received task: {task}")

        if task == "scan_and_go" and self.state == "IDLE":
            self.state = "ROTATE"
            self.ticks_left = int(self.rotate_time / self.dt)
            self.publish_status("TB3: starting scan (rotate 2s)")
        else:
            self.get_logger().info(f"Ignored task '{task}' (state={self.state})")

    def on_scan(self, scan: LaserScan):
        angle_min = scan.angle_min
        angle_inc = scan.angle_increment
        n = len(scan.ranges)
        cone = math.radians(self.front_angle_deg)

        blocked = False
        for i in range(n):
            ang = angle_min + i * angle_inc
            if -cone <= ang <= cone:
                r = scan.ranges[i]
                if math.isfinite(r) and r > 0.0 and r < self.safe_dist:
                    blocked = True
                    break

        self.blocked = blocked

    def stop(self):
        self.cmd_pub.publish(Twist())

    def on_timer(self):
        if self.state == "IDLE":
            self.stop()
            return

        tw = Twist()

        if self.state == "ROTATE":
            tw.angular.z = self.turn_speed
            self.cmd_pub.publish(tw)

            self.ticks_left -= 1
            if self.ticks_left <= 0:
                self.state = "GO"
                self.ticks_left = int(self.go_time / self.dt)
                self.publish_status("TB3: scan done -> moving forward (safe go 4s)")
            return

        if self.state == "GO":
            # safety logic
            if self.blocked:
                tw.linear.x = 0.0
                tw.angular.z = self.turn_speed
            else:
                tw.linear.x = self.fwd_speed
                tw.angular.z = 0.0

            self.cmd_pub.publish(tw)
            self.ticks_left -= 1

            if self.ticks_left <= 0:
                self.state = "IDLE"
                self.stop()
                self.publish_status("TB3: arrived")
                self.get_logger().info("TB3 motion done -> published arrived")
            return


def main():
    rclpy.init()
    node = TB3Coordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

