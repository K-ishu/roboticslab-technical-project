from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
import os


def generate_launch_description():
    home = os.path.expanduser('~')

    world_file = os.path.join(
        home,
        'roboticslab-technical-project',
        'worlds',
        'lab_world.sdf'
    )

    rsp_yaml = os.path.join(
        home,
        'roboticslab-technical-project',
        'ros2_ws',
        'src',
        'multi_robot_coop',
        'config',
        'iiwa_rsp.yaml'
    )

    return LaunchDescription([
        # ---------- Gazebo ----------
        ExecuteProcess(
            cmd=[
                'gazebo',
                '--verbose',
                '-s', 'libgazebo_ros_init.so',
                '-s', 'libgazebo_ros_factory.so',
                world_file
            ],
            output='screen'
        ),

        # ---------- Robot State Publisher ----------
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[rsp_yaml],
            output='screen'
        ),

        # ---------- Controllers ----------
        TimerAction(
            period=5.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
                    output='screen'
                )
            ]
        ),
        TimerAction(
            period=7.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'iiwa_arm_controller'],
                    output='screen'
                )
            ]
        ),

        # ---------- Scenario Coordinator ----------
        TimerAction(
            period=9.0,
            actions=[
                Node(
                    package='multi_robot_coop',
                    executable='scenario_coordinator',
                    output='screen'
                )
            ]
        ),
    ])

