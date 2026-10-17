# Vayuputra TF2 Frame Structure

## 1. Purpose

This document defines the TF2 coordinate-frame structure for the Vayuputra
AirMouse ROS 2 system.

The TF2 structure provides a common coordinate relationship between:

- Global SLAM map
- UAV odometry
- UAV body
- LiDAR
- RealSense camera
- IMU

This allows sensor data, SLAM results, navigation goals and survivor
detections to be represented in consistent coordinate frames.

---

## 2. TF2 Frame Tree

The initial Vayuputra TF2 structure is:

```text
map
└── odom
    └── base_link
        ├── base_footprint
        ├── lidar_link
        ├── camera_link
        │   └── camera_depth_frame
        └── imu_link