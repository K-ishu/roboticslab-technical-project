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

### Environment Includes

- Static boundary walls  
- Obstacle box  
- Obstacle cylinder  
- Dynamic cylindrical stone  
- Placement container  
- TurtleBot3 Waffle Pi  
- KUKA LBR iiwa with ROS2 Control  
- Custom Gazebo physics interaction  

---

### Important World Coordinates

#### Arm Base
```txt id="rdff5u"
(-1.3, -0.3, 0)

```

#  ROS2 GAZEBO MULTI-ROBOT SYSTEM


## Simulation Environment

### Environment Includes
- Static boundary walls
- Obstacle box
- Obstacle cylinder
- Dynamic cylindrical stone
- Placement container
- TurtleBot3 Waffle Pi
- KUKA LBR iiwa with ROS2 Control
- Custom Gazebo physics interaction

# ------------------------------------------------------------------------------

### Important World Coordinates

#### Container Center
(-1.54015, -1.08473, 0)

#### Obstacle Box
(1.51611, -3.24702, 0.25)

#### Obstacle Cylinder
(2.87436, -2.43085, 0.35)

-----------------------------------------------------------------------------------------------
#ROBOT SYSTEMS


## TurtleBot3 Waffle Pi

### ROS2 Topics
/cmd_vel
/odom
/tb3/scan

### Features
- Differential drive motion
- 2D 360° LiDAR sensing
- Sector-based obstacle avoidance
- Stone alignment
- Reactive navigation
- Stuck detection
- Recovery behavior

# ------------------------------------------------------------------------------

## KUKA LBR iiwa

### Controller Topic
/iiwa_arm_controller/joint_trajectory

### Active Controllers
joint_state_broadcaster
iiwa_arm_controller

### End-Effector / Tool Link
lbr_iiwa_tool

### Features
- 7-DOF serial manipulator
- ROS2 Control integration
- Joint trajectory execution
- Simulated grasping via Gazebo link attachment
- Pick-and-place operation


#SYSTEM ARCHITECTURE


## Main Coordinator Node
scenario_coordinator

### Description
The scenario_coordinator node manages the complete autonomous mission
using a finite state machine (FSM).

# ------------------------------------------------------------------------------

### Core Topics
/scenario_status
/tb3/scan
/odom
/cmd_vel
/iiwa_arm_controller/joint_trajectory

### Services
/attach
/detach

### Service Type
gazebo_ros_link_attacher/Attach

--------------------------------------------------------------------------------
#GAZEBO LINK ATTACHER
--------------------------------------------------------------------------------

## Purpose
Used to simulate robotic grasping and object transport between robots and stone.

### Attach Examples

#### TurtleBot3 transporting stone
tb3::base_link  <->  stone::stone_link

#### KUKA iiwa grasping stone
lbr_iiwa::lbr_iiwa_tool  <->  stone::stone_link


#VERIFICATION COMMANDS


## 1. Verify Gazebo Link Attacher
$ ros2 service list | grep attach

Expected Output:
/attach
/detach

# ------------------------------------------------------------------------------

## 2. Verify ROS2 Controllers
$ ros2 control list_controllers

Expected Output:
joint_state_broadcaster [active]
iiwa_arm_controller [active]

# ------------------------------------------------------------------------------

## 3. Verify TurtleBot3 LiDAR
$ ros2 topic echo /tb3/scan

Expected Output:
sensor_msgs/msg/LaserScan
ranges: [...]
angle_min: ...
angle_max: ...

# ------------------------------------------------------------------------------

## 4. Verify Odometry
$ ros2 topic echo /odom

Expected Output:
nav_msgs/msg/Odometry
position:
x: ...
y: ...
orientation: ...

# ------------------------------------------------------------------------------

## 5. Verify Scenario Status
$ ros2 topic echo /scenario_status

Expected Output Example:
SEARCHING_STONE
ALIGNING
TRANSPORTING
PICKING
PLACING
COMPLETE

# ------------------------------------------------------------------------------

## 6. Send TurtleBot3 Velocity Command
$ ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "
linear:
  x: 0.2
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
"

Expected Behavior:
TurtleBot3 moves forward

# ------------------------------------------------------------------------------

## 7. Send KUKA Joint Trajectory
$ ros2 topic pub /iiwa_arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "
joint_names:
- A1
- A2
- A3
- A4
- A5
- A6
- A7
points:
- positions: [0.0, -0.5, 0.0, -1.0, 0.0, 1.0, 0.0]
  time_from_start:
    sec: 3
"

Expected Behavior:
KUKA iiwa moves to target configuration

# ------------------------------------------------------------------------------

## 8. Attach Stone to TurtleBot3
$ ros2 service call /attach gazebo_ros_link_attacher/srv/Attach "
model_name_1: 'tb3'
link_name_1: 'base_link'
model_name_2: 'stone'
link_name_2: 'stone_link'
"

Expected Output:
success: True

# ------------------------------------------------------------------------------

## 9. Detach Stone
$ ros2 service call /detach gazebo_ros_link_attacher/srv/Attach "
model_name_1: 'tb3'
link_name_1: 'base_link'
model_name_2: 'stone'
link_name_2: 'stone_link'
"

Expected Output:
success: True


#COMPLETE MISSION FLOW


1. TurtleBot3 scans environment
2. Detects stone using LiDAR
3. Aligns with stone
4. Attaches stone
5. Navigates to KUKA workspace
6. KUKA grasps stone
7. TurtleBot3 detaches
8. KUKA places stone into container
9. Mission complete


#PROJECT HIGHLIGHTS


- Multi-robot coordination
- ROS2 + Gazebo integration
- Autonomous mobile manipulation
- Finite State Machine control
- Sector-based obstacle avoidance
- Simulated grasping
- Pick-and-place pipeline
- Full mission autonomy

