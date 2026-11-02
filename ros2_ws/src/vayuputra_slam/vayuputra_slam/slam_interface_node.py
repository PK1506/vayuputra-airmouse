import rclpy
from rclpy.node import Node

from nav_msgs.msg import OccupancyGrid, Odometry
from geometry_msgs.msg import PoseStamped


class SlamInterfaceNode(Node):

    def __init__(self):
        super().__init__('slam_interface_node')

        self.declare_parameter('map_topic', '/slam/map')
        self.declare_parameter('map_message_type', 'nav_msgs/msg/OccupancyGrid')

        self.declare_parameter('pose_topic', '/slam/pose')
        self.declare_parameter('pose_message_type', 'geometry_msgs/msg/PoseStamped')

        self.declare_parameter('odometry_topic', '/slam/odometry')
        self.declare_parameter('odometry_message_type', 'nav_msgs/msg/Odometry')

        self.get_logger().info('SLAM interface configuration:')

        for name in (
            'map_topic',
            'map_message_type',
            'pose_topic',
            'pose_message_type',
            'odometry_topic',
            'odometry_message_type',
        ):
            value = self.get_parameter(name).value
            self.get_logger().info(f'{name}: {value}')


def main(args=None):
    rclpy.init(args=args)
    node = SlamInterfaceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
