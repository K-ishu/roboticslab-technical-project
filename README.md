Multi-Robot Cooperative System in Gazebo (ROS 2 Humble)
Robotics Lab – Technical Project 2026

This repository contains a case-study implementation of a cooperative multi-robot autonomous system simulated in Gazebo Classic using ROS 2 Humble.

The system demonstrates coordination between a mobile robot (TurtleBot3) and an industrial manipulator (KUKA LBR iiwa) to accomplish a transport and pick-and-place task in a custom simulation environment.



1 Problem Description

The objective of this project is to design and simulate an autonomous interactive multi-robot system in which:

1.A mobile robot navigates in a cluttered environment.

2.It approaches and captures a movable object.

3.It transports the object to a predefined handover zone.

4.An industrial robotic arm grasps the object.

5.The arm places the object inside a container.

6.The mobile robot returns to its initial position.

This scenario represents a simplified industrial logistics workflow involving robot collaboration.


2. Simulation Setup
Custom Gazebo World

World file:  
worlds/lab_world.sdf

The world includes:

Boundary brick walls

Ground plane

A movable stone object

A cylindrical container (target placement area)

Static obstacle box

Static obstacle cylinder

TurtleBot3 Waffle Pi

KUKA LBR iiwa (ros2_control enabled).       


Important Object Poses

| Element           | Pose                      |
| ----------------- | ------------------------- |
| Arm base          | (-1.3, -0.3, 0)           |
| Container         | (-1.54015, -1.08473, 0)   |
| Obstacle box      | (1.51611, -3.24702, 0.25) |
| Obstacle cylinder | (2.87436, -2.43085, 0.35) |


Robots
TurtleBot3 (Differential Drive)

Motion control via /cmd_vel

Odometry feedback via /odom

LiDAR sensor via /tb3/scan

Reactive obstacle avoidance

Stone attach/detach capability using Gazebo link attacher


KUKA LBR iiwa (Industrial Arm)

Controlled using ros2_control

Joint trajectory interface

/iiwa_arm_controller/joint_trajectory

End-effector grasp simulated via dynamic link attachment

