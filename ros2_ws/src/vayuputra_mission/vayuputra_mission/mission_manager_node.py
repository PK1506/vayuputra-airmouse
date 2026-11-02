import rclpy
from rclpy.node import Node

from vayuputra_interfaces.srv import MissionCommand


class MissionManagerNode(Node):

    def __init__(self):
        super().__init__('mission_manager_node')

        self.mission_state = 'idle'

        self.service = self.create_service(
            MissionCommand,
            '/mission/command',
            self.handle_command
        )

        self.get_logger().info(
            'Mission Manager ready. Service: /mission/command'
        )

    def handle_command(self, request, response):
        command = request.command.strip().lower()

        if not request.mission_id.strip():
            response.accepted = False
            response.message = 'mission_id must not be empty'

        elif command == 'start':
            if self.mission_state == 'running':
                response.accepted = False
                response.message = 'Mission is already running'
            else:
                self.mission_state = 'running'
                response.accepted = True
                response.message = (
                    f'Mission {request.mission_id} marked as running'
                )

        elif command == 'pause':
            if self.mission_state != 'running':
                response.accepted = False
                response.message = 'Only a running mission can be paused'
            else:
                self.mission_state = 'paused'
                response.accepted = True
                response.message = (
                    f'Mission {request.mission_id} marked as paused'
                )

        elif command == 'stop':
            self.mission_state = 'idle'
            response.accepted = True
            response.message = (
                f'Mission {request.mission_id} marked as stopped'
            )

        else:
            response.accepted = False
            response.message = (
                'Unsupported command. Use start, pause, or stop'
            )

        self.get_logger().info(
            f'Command={command}, state={self.mission_state}, '
            f'accepted={response.accepted}'
        )

        return response


def main(args=None):
    rclpy.init(args=args)
    node = MissionManagerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
