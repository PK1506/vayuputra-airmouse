from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_lidar',
            arguments=[
                '0', '0', '0',
                '0', '0', '0',
                'base_link',
                'lidar_link'
            ],
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_camera',
            arguments=[
                '0', '0', '0',
                '0', '0', '0',
                'base_link',
                'camera_link'
            ],
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_imu',
            arguments=[
                '0', '0', '0',
                '0', '0', '0',
                'base_link',
                'imu_link'
            ],
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='camera_to_depth',
            arguments=[
                '0', '0', '0',
                '0', '0', '0',
                'camera_link',
                'camera_depth_frame'
            ],
        ),
    ])