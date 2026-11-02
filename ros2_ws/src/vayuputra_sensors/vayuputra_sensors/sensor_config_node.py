import rclpy
from rclpy.node import Node


class SensorConfigNode(Node):
    def __init__(self):
        super().__init__('sensor_config_node')

        self.declare_parameter(
            'lidar_topic',
            '/sensors/lidar/points'
        )
        self.declare_parameter(
            'lidar_message_type',
            'sensor_msgs/msg/PointCloud2'
        )

        self.declare_parameter(
            'imu_topic',
            '/sensors/imu/data'
        )
        self.declare_parameter(
            'imu_message_type',
            'sensor_msgs/msg/Imu'
        )

        self.declare_parameter(
            'camera_image_topic',
            '/sensors/camera/image'
        )
        self.declare_parameter(
            'camera_image_message_type',
            'sensor_msgs/msg/Image'
        )

        self.declare_parameter(
            'camera_info_topic',
            '/sensors/camera/camera_info'
        )
        self.declare_parameter(
            'camera_info_message_type',
            'sensor_msgs/msg/CameraInfo'
        )
        self.declare_parameter(
            'depth_image_topic',
            '/sensors/depth/image'
        )
        self.declare_parameter(
            'depth_image_message_type',
            'sensor_msgs/msg/Image'
        )

        for name in (
            'lidar_topic',
            'lidar_message_type',
            'imu_topic',
            'imu_message_type',
            'camera_image_topic',
            'camera_image_message_type',
            'camera_info_topic',
            'camera_info_message_type',
            'depth_image_topic',
            'depth_image_message_type',
        ):
            value = self.get_parameter(name).value
            self.get_logger().info(f'{name}: {value}')


def main(args=None):
    rclpy.init(args=args)
    node = SensorConfigNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
