from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
import os


def generate_launch_description():
    world_file = os.path.join(
        os.path.expanduser('~'),
        'roboticslab-technical-project',
        'worlds',
        'lab_world.sdf'
    )

    # --- Gazebo Classic ---
    gazebo = ExecuteProcess(
        cmd=[
            'gazebo', '--verbose',
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so',
            world_file
        ],
        output='screen'
    )

    # --- robot_state_publisher (برای gazebo_ros2_control لازم است) ---
    rsp_yaml = os.path.join(
        os.path.expanduser('~'),
        'roboticslab-technical-project',
        'ros2_ws', 'src', 'multi_robot_coop', 'config', 'iiwa_rsp.yaml'
    )

    rsp = TimerAction(
        period=2.0,
        actions=[
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                parameters=[rsp_yaml],
                output='screen'
            )
        ]
    )

    # --- Load controllers (خیلی مهم برای اینکه بازو واقعاً حرکت کند) ---
    # اگر نام کنترلرها در پروژه‌ات فرق دارد همینجا اسم‌ها را عوض کن.
    load_jsb = TimerAction(
        period=6.0,
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
                output='screen'
            )
        ]
    )

    load_arm = TimerAction(
        period=8.0,
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'iiwa_arm_controller'],
                output='screen'
            )
        ]
    )

    # --- Scenario Coordinator ---
    scenario = TimerAction(
        period=10.0,
        actions=[
            Node(
                package='multi_robot_coop',
                executable='scenario_coordinator',
                output='screen',
                parameters=[
                    # topics
                    {"odom_topic": "/odom"},
                    {"scan_topic": "/tb3/scan"},
                    {"cmd_vel_topic": "/cmd_vel"},

                    # gazebo link-attacher services
                    {"attach_service": "/attach"},
                    {"detach_service": "/detach"},
                    {"tb3_model": "tb3"},
                    {"tb3_link": "tb3::base_link"},
                    {"stone_model": "stone"},
                    {"stone_link": "stone::stone_link"},

                    # positions (از خودت)
                    {"stone_xy": [3.45662, -0.223026]},
                    {"arm_xy": [-1.3, -0.3]},
                    {"container_xy": [-1.54015, -1.08473]},

                    # obstacles (برای اینکه avoid منطقی‌تر شود)
                    {"obstacle_box_xy": [1.51611, -3.24702]},
                    {"obstacle_cyl_xy": [2.87436, -2.43085]},

                    # speed tuning
                    {"v_go": 0.30},
                    {"v_touch": 0.08},
                    {"v_push": 0.22},
                    {"w_max": 1.2},

                    # attach / detach tuning
                    {"attach_dist": 0.14},          # نزدیک‌تر برای “gap دیده نشه”
                    {"attach_center_tol_deg": 4.0},
                    {"arm_drop_offset_x": 0.25},    # سنگ را جلوی بازو بینداز
                    {"arm_stop_dist": 0.22},
                ]
            )
        ]
    )

    return LaunchDescription([
        gazebo,
        rsp,
        load_jsb,
        load_arm,
        scenario,
    ])

