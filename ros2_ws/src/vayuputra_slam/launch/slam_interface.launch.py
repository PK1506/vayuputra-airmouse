from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_dir = get_package_share_directory('vayuputra_slam')
    config_file = os.path.join(
        package_dir,
        'config',
        'slam_topics.yaml'
    )

    slam_interface_node = Node(
        package='vayuputra_slam',
        executable='slam_interface_node',
        name='slam_interface_node',
        output='screen',
        parameters=[config_file]
    )

    return LaunchDescription([
        slam_interface_node
    ])
