import rclpy
from rclpy.node import Node


class NavigationInterfaceNode(Node):

    def __init__(self):
        super().__init__('navigation_interface_node')

        parameters = {
            'goal_topic': '/navigation/goal',
            'goal_message_type': 'geometry_msgs/msg/PoseStamped',
            'cmd_vel_topic': '/navigation/cmd_vel',
            'cmd_vel_message_type': 'geometry_msgs/msg/Twist',
            'status_topic': '/navigation/status',
            'status_message_type': 'std_msgs/msg/String',
            'navigate_action': '/navigate_to',
            'navigate_action_type': 'nav2_msgs/action/NavigateToPose',
        }

        for name, default_value in parameters.items():
            self.declare_parameter(name, default_value)

        self.get_logger().info('Navigation interface configuration:')

        for name in parameters:
            value = self.get_parameter(name).value
            self.get_logger().info(f'{name}: {value}')


def main(args=None):
    rclpy.init(args=args)
    node = NavigationInterfaceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
