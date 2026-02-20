
# Robotics Lab – Technical Project
-----------------------------------------------------------------------
**PROJECT OVERVIEW**
<img width="1351" height="713" alt="overview" src="https://github.com/user-attachments/assets/9b1f4f93-5139-4d63-a4dc-7001664e32b5" />

This repository contains a case-study implementation of a cooperative
multi-robot autonomous system simulated in Gazebo Classic using ROS 2 Humble.

The system demonstrates collaboration between:

- TurtleBot3 Waffle Pi (mobile differential drive robot)
- KUKA LBR iiwa industrial manipulator

The objective is to execute a complete cooperative workflow including:
navigation, object transport, grasping, and placement.

-----------------------------------------------------------------------

**CASE STUDY DESCRIPTION**

1) TurtleBot3 navigates autonomously using LiDAR.
2) TurtleBot3 aligns with a stone object.
3) The stone is attached using gazebo_ros_link_attacher.
4) TurtleBot3 transports the stone near the robotic arm.
5) The stone is detached in a predefined pick position.
6) The robotic arm executes a joint trajectory.
7) The arm grasps the stone (attach to end-effector).
8) The arm places the stone inside a container.
9) TurtleBot3 returns to its initial position.

-----------------------------------------------------------------------

**SIMULATION ENVIRONMENT**

World file:
worlds/lab_world.sdf

The environment includes:
- Static boundary walls
- Obstacle box
- Obstacle cylinder
- Cylindrical stone (dynamic object)
- Container (placement target)
- TurtleBot3 Waffle Pi
- KUKA LBR iiwa (ros2_control enabled)

**Important poses:**

Arm Base:
(-1.3, -0.3, 0)

Container:
(-1.54015, -1.08473, 0)

Obstacle Box:
(1.51611, -3.24702, 0.25)

Obstacle Cylinder:
(2.87436, -2.43085, 0.35)

-----------------------------------------------------------------------

**ROBOTS**

TurtleBot3:
- /cmd_vel
- /odom
- /tb3/scan
- Reactive obstacle avoidance
- Stuck detection and recovery

**KUKA LBR iiwa:**
- ros2_control enabled
- joint_trajectory_controller
- /iiwa_arm_controller/joint_trajectory
- End-effector link:
  lbr_iiwa::lbr_iiwa_link_7

-----------------------------------------------------------------------

**SYSTEM ARCHITECTURE**

Main Node:
scenario_coordinator
```ros2 topic list```
Topics:
- /cmd_vel
- /odom
- /tb3/scan
- /iiwa_arm_controller/joint_trajectory
- /scenario_status

Services:
- /attach
- /detach

Service type:
```gazebo_ros_link_attacher/Attach```
![5816888498236100159](https://github.com/user-attachments/assets/10fbd90a-8398-4f18-97c0-2027203aef3b)

-----------------------------------------------------------------------
**controllers**

```ros2 control list_controllers```
```joint_state_broadcaster[active]```
```iiwa_arm_controller[active]```
------------------------------------------------------------------------
**CONTROL LOGIC**

TurtleBot3:
- Sector-based LiDAR avoidance
- Speed scaling
- Angular correction
- Recovery behavior

Stone Alignment:
- Front-cone LaserScan detection
- Angle minimization
- Slow approach
- Hard stop before attach

Arm Pick & Place:
- Fix stone pose to grasp position
- Publish joint trajectory
- Attach stone to EE link
- Move to container
- Fix placement pose
- Detach

-----------------------------------------------------------------------

**STATE MACHINE**

1) TB3_GOTO_STONE_AREA
2) TB3_TOUCH_AND_ATTACH
3) ATTACH
4) TB3_PUSH_TO_ARM
5) TB3_DETACH_NEAR_ARM
6) ARM_PICK_PLACE
7) TB3_GOTO_HOME
8) DONE

Monitor state:

```ros2 topic echo /scenario_status```

-----------------------------------------------------------------------

**LAUNCH INSTRUCTIONS**
```
cd ~/roboticslab-technical-project/ros2_ws
colcon build
source install/setup.bash
ros2 launch multi_robot_coop scenario.launch.py
```
-----------------------------------------------------------------------

**DEPENDENCIES**

Ubuntu 22.04
ROS 2 Humble
Gazebo Classic
gazebo_ros
gazebo_ros_link_attacher
ros2_control
joint_state_broadcaster
joint_trajectory_controller

-----------------------------------------------------------------------

**RESULTS**

The system successfully demonstrates:

- Autonomous navigation
- Obstacle avoidance
- Service-based multi-robot cooperation
- Industrial arm manipulation
- Coordinated pick-and-place

-----------------------------------------------------------------------

**VIDEO DEMO**


https://github.com/user-attachments/assets/0ccdeb76-6b2c-4dc8-870e-92841887adc4

because of the system problem the gazebo crashed and you can see just first part of cooperation
-----------------------------------------------------------------------

**AUTHOR**

Name: Mohammad reza khodashenas
Course: Robotics Lab – Technical Project  professor:Mario salvegio
Year: 2026

-----------------------------------------------------------------------
