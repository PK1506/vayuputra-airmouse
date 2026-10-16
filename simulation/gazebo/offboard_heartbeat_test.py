#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint


class OffboardHeartbeatTest(Node):
    def __init__(self):
        super().__init__("offboard_heartbeat_test")

        self.mode_pub = self.create_publisher(
            OffboardControlMode,
            "/fmu/in/offboard_control_mode",
            10,
        )
        self.setpoint_pub = self.create_publisher(
            TrajectorySetpoint,
            "/fmu/in/trajectory_setpoint",
            10,
        )

        self.timer = self.create_timer(0.05, self.publish_setpoints)
        self.get_logger().info(
            "Publishing position-mode heartbeat at 20 Hz. "
            "No arming or mode-change commands will be sent."
        )

    def publish_setpoints(self):
        timestamp = self.get_clock().now().nanoseconds // 1000

        mode = OffboardControlMode()
        mode.timestamp = timestamp
        mode.position = True
        self.mode_pub.publish(mode)

        setpoint = TrajectorySetpoint()
        setpoint.timestamp = timestamp
        setpoint.position = [0.0, 0.0, -0.5]
        setpoint.velocity = [math.nan, math.nan, math.nan]
        setpoint.acceleration = [math.nan, math.nan, math.nan]
        setpoint.jerk = [math.nan, math.nan, math.nan]
        setpoint.yaw = math.nan
        setpoint.yawspeed = math.nan
        self.setpoint_pub.publish(setpoint)


def main():
    rclpy.init()
    node = OffboardHeartbeatTest()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
