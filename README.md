# Robotics Lab – Technical Project  
## Cooperative Multi-Robot Autonomous System using ROS 2 Humble + Gazebo Classic

---

## Project Overview

This repository presents a cooperative autonomous multi-robot system developed using ROS 2 Humble and Gazebo Classic.

The system demonstrates collaboration between:

- TurtleBot3 Waffle Pi — mobile differential-drive robot
- KUKA LBR iiwa — 7-DOF industrial manipulator

The objective is to execute a complete autonomous workflow involving navigation, object detection, object transport, robot-to-robot handover, grasping, and container placement.

---

## System Objective

The goal of this project is to demonstrate an autonomous industrial-style cooperation scenario where:

1. TurtleBot3 navigates inside a custom Gazebo world.
2. TurtleBot3 detects and aligns with a stone object using LiDAR.
3. The stone is attached to TurtleBot3 using gazebo_ros_link_attacher.
4. TurtleBot3 transports the stone to the robotic arm workspace.
5. TurtleBot3 detaches the stone at a predefined handover position.
6. KUKA LBR iiwa executes a joint trajectory.
7. The arm grasps the stone using a simulated link attachment.
8. The arm places the stone into a target container.
9. TurtleBot3 returns to its initial position.

---

## Simulation Environment

### World File

```bash
worlds/lab_world.sdf

```


