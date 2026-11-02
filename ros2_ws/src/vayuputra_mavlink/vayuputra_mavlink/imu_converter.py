import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from px4_msgs.msg import SensorCombined
from sensor_msgs.msg import Imu


class IMUConverter(Node):
    def __init__(self):
        super().__init__('px4_imu_converter')

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.subscription = self.create_subscription(
            SensorCombined,
            '/fmu/out/sensor_combined',
            self.imu_callback,
            qos
        )

        self.publisher = self.create_publisher(
            Imu,
            '/sensors/imu/data',
            10
        )

        self.get_logger().info('PX4 IMU Converter started')

    def imu_callback(self, msg):
        imu = Imu()
        imu.header.stamp = self.get_clock().now().to_msg()
        imu.header.frame_id = 'imu_link'

        # SensorCombined does not provide orientation.
        imu.orientation_covariance[0] = -1.0

        # Convert PX4 FRD body axes to ROS FLU body axes.
        imu.angular_velocity.x = float(msg.gyro_rad[0])
        imu.angular_velocity.y = -float(msg.gyro_rad[1])
        imu.angular_velocity.z = -float(msg.gyro_rad[2])

        imu.linear_acceleration.x = float(msg.accelerometer_m_s2[0])
        imu.linear_acceleration.y = -float(msg.accelerometer_m_s2[1])
        imu.linear_acceleration.z = -float(msg.accelerometer_m_s2[2])

        self.publisher.publish(imu)


def main(args=None):
    rclpy.init(args=args)
    node = IMUConverter()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
