from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Path to your world inside the repo (NOT inside the ROS package)
    world_path = '/home/kishu/roboticslab-technical-project/worlds/lab_world.sdf'

    # Environment settings for VirtualBox + Gazebo resources
    gz_env = {
        'LIBGL_ALWAYS_SOFTWARE': '1',
        'GZ_PARTITION': 'lab',
        'GZ_IP': '127.0.0.1',
        'GZ_SIM_RESOURCE_PATH': '/opt/ros/jazzy/share:/home/kishu/roboticslab-technical-project',
    }

    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-v', '4', world_path],
        output='screen',
        additional_env=gz_env
    )

    mobile = Node(
        package='roboticslab_project',
        executable='mobile_controller',
        output='screen'
    )

    arm = Node(
        package='roboticslab_project',
        executable='arm_controller',
        output='screen'
    )

    # Optional: bridge /clock to ROS2 (useful for rosbag / timing)
    clock_bridge = ExecuteProcess(
        cmd=['ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
             '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        clock_bridge,
        mobile,
        arm,
    ])
