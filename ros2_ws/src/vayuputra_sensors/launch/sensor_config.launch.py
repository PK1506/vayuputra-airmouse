from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_dir = get_package_share_directory('vayuputra_sensors')
    config_file = os.path.join(
        package_dir,
        'config',
        'sensor_topics.yaml'
    )

    return LaunchDescription([
        Node(
            package='vayuputra_sensors',
            executable='sensor_config_node',
            name='sensor_config_node',
            output='screen',
            parameters=[config_file],
        )
    ])