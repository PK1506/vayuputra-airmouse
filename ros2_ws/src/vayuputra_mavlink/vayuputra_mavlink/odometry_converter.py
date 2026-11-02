import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from px4_msgs.msg import VehicleOdometry
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class OdometryConverter(Node):

    def __init__(self):
        super().__init__('px4_odometry_converter')

        # QoS compatible with PX4 odometry publisher
        px4_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Subscribe to PX4 vehicle odometry
        self.subscription = self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.odometry_callback,
            px4_qos
        )

        # Publish ROS odometry
        self.publisher = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        # Broadcast dynamic odom -> base_link transform
        self.tf_broadcaster = TransformBroadcaster(self)

        self.get_logger().info('PX4 Odometry Converter started')

    def odometry_callback(self, msg):

        # Check coordinate frames
        if msg.pose_frame != VehicleOdometry.POSE_FRAME_NED:
            self.get_logger().warning('Pose frame is not NED')
            return

        if msg.velocity_frame != VehicleOdometry.VELOCITY_FRAME_NED:
            self.get_logger().warning('Velocity frame is not NED')
            return

        # 1. POSITION: NED -> ENU
        north, east, down = map(float, msg.position)

        x = east
        y = north
        z = -down

        # 2. ORIENTATION: NED/FRD -> ENU/FLU
        # PX4 quaternion format: [w, x, y, z]
        w, qx, qy, qz = map(float, msg.q)

        norm = math.sqrt(w*w + qx*qx + qy*qy + qz*qz)

        if not math.isfinite(norm) or norm < 1e-6:
            self.get_logger().warning('Invalid PX4 quaternion')
            return

        # Normalize quaternion
        w /= norm
        qx /= norm
        qy /= norm
        qz /= norm

        s = math.sqrt(0.5)

        # q_ENU_NED * q_PX4
        a_w = -s * qx - s * qy
        a_x = s * w + s * qz
        a_y = s * w - s * qz
        a_z = s * qx - s * qy

        # Result * q_FRD_FLU
        qw = -a_x
        qx_ros = a_w
        qy_ros = a_z
        qz_ros = -a_y

        # 3. CREATE ODOMETRY MESSAGE
        odom = Odometry()

        # Use ROS receive time
        odom.header.stamp = self.get_clock().now().to_msg()

        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.position.z = z

        odom.pose.pose.orientation.w = qw
        odom.pose.pose.orientation.x = qx_ros
        odom.pose.pose.orientation.y = qy_ros
        odom.pose.pose.orientation.z = qz_ros

        # 4. LINEAR VELOCITY: NED -> ENU -> BASE_LINK
        vn, ve, vd = map(float, msg.velocity)

        vx = ve
        vy = vn
        vz = -vd

        # Rotate ENU velocity into base_link using inverse orientation
        t_x = -2.0 * (qy_ros * vz - qz_ros * vy)
        t_y = -2.0 * (qz_ros * vx - qx_ros * vz)
        t_z = -2.0 * (qx_ros * vy - qy_ros * vx)

        odom.twist.twist.linear.x = (
            vx + qw * t_x - qy_ros * t_z + qz_ros * t_y
        )

        odom.twist.twist.linear.y = (
            vy + qw * t_y - qz_ros * t_x + qx_ros * t_z
        )

        odom.twist.twist.linear.z = (
            vz + qw * t_z - qx_ros * t_y + qy_ros * t_x
        )

        # 5. ANGULAR VELOCITY: FRD -> FLU
        wx, wy, wz = map(float, msg.angular_velocity)

        odom.twist.twist.angular.x = wx
        odom.twist.twist.angular.y = -wy
        odom.twist.twist.angular.z = -wz

        # Publish odometry
        self.publisher.publish(odom)

        # 6. PUBLISH DYNAMIC TF: odom -> base_link
        tf = TransformStamped()

        tf.header = odom.header
        tf.child_frame_id = 'base_link'

        tf.transform.translation.x = x
        tf.transform.translation.y = y
        tf.transform.translation.z = z

        tf.transform.rotation = odom.pose.pose.orientation

        self.tf_broadcaster.sendTransform(tf)


def main(args=None):

    rclpy.init(args=args)

    node = OdometryConverter()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()