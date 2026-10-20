import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_dir = get_package_share_directory(
        'vayuputra_navigation'
    )

    config_file = os.path.join(
        package_dir,
        'config',
        'navigation_topics.yaml'
    )

    navigation_node = Node(
        package='vayuputra_navigation',
        executable='navigation_interface_node',
        name='navigation_interface_node',
        output='screen',
        parameters=[config_file],
    )

    return LaunchDescription([navigation_node])
