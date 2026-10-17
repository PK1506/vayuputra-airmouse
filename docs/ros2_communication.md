# Vayuputra ROS 2 Communication Specification

## 1. Purpose

This document defines the ROS 2 communication interfaces required for the
Vayuputra AirMouse system.

The communication architecture connects:

- Sensors
- SLAM and localization
- Navigation
- Autonomous exploration
- Survivor detection
- Mission management
- MAVROS / PX4 integration
- Ground Control Station (GCS)

The architecture is designed for GPS-denied indoor autonomous search and rescue.

---

## 2. Communication Model

Vayuputra uses three ROS 2 communication mechanisms:

### Topics

Topics are used for continuous or streaming data such as:

- Sensor measurements
- Robot pose
- Maps
- Detection results
- Navigation state
- Exploration state

### Services

Services are used for short request/response operations such as:

- Vehicle arming
- Vehicle disarming
- Flight mode changes
- Mission control commands

### Actions

Actions are used for long-running operations that require feedback and a final
result, such as:

- Navigation to a target
- Autonomous exploration
- Complete mission execution

---

# 3. ROS 2 Topics

## 3.1 Sensor Topics

| Topic | Purpose | Publisher | Subscriber | Message Type |
|---|---|---|---|---|
| `/sensors/lidar/points` | Livox MID-360 point cloud | `vayuputra_sensors` | `vayuputra_slam` | `sensor_msgs/msg/PointCloud2` |
| `/sensors/depth/image` | RealSense D455 depth data | `vayuputra_sensors` | `vayuputra_slam`, `vayuputra_detection` | `sensor_msgs/msg/Image` |
| `/sensors/camera/image` | RealSense camera image | `vayuputra_sensors` | `vayuputra_detection` | `sensor_msgs/msg/Image` |
| `/sensors/imu/data` | Flight-controller IMU data | `vayuputra_sensors` / MAVROS | `vayuputra_slam` | `sensor_msgs/msg/Imu` |

---

## 3.2 SLAM and Localization Topics

| Topic | Purpose | Publisher | Subscriber | Message Type |
|---|---|---|---|---|
| `/slam/map` | 2D occupancy grid map | `vayuputra_slam` | `vayuputra_navigation`, `vayuputra_exploration`, GCS | `nav_msgs/msg/OccupancyGrid` |
| `/slam/pose` | Estimated UAV pose | `vayuputra_slam` | `vayuputra_navigation`, `vayuputra_mission` | `geometry_msgs/msg/PoseStamped` |
| `/slam/odometry` | Estimated UAV motion | `vayuputra_slam` | `vayuputra_navigation`, `vayuputra_mission` | `nav_msgs/msg/Odometry` |

---

## 3.3 Navigation Topics

| Topic | Purpose | Publisher | Subscriber | Message Type |
|---|---|---|---|---|
| `/navigation/goal` | Current navigation target | `vayuputra_exploration` / `vayuputra_mission` | `vayuputra_navigation` | `geometry_msgs/msg/PoseStamped` |
| `/navigation/cmd_vel` | Navigation velocity command | `vayuputra_navigation` | MAVROS / flight-control layer | `geometry_msgs/msg/Twist` |
| `/navigation/status` | Current navigation state | `vayuputra_navigation` | `vayuputra_mission`, GCS | `std_msgs/msg/String` |

---

## 3.4 Exploration Topics

| Topic | Purpose | Publisher | Subscriber | Message Type |
|---|---|---|---|---|
| `/exploration/frontiers` | Detected unexplored map regions | `vayuputra_exploration` | `vayuputra_exploration`, GCS | TBD |
| `/exploration/next_best_view` | Selected next-best-view target | `vayuputra_exploration` | `vayuputra_navigation` | `geometry_msgs/msg/PoseStamped` |
| `/exploration/status` | Exploration state and progress | `vayuputra_exploration` | `vayuputra_mission`, GCS | `std_msgs/msg/String` |

---

## 3.5 Survivor Detection Topics

| Topic | Purpose | Publisher | Subscriber | Message Type |
|---|---|---|---|---|
| `/detection/survivors` | Detected survivor information | `vayuputra_detection` | `vayuputra_mission`, GCS | `vayuputra_interfaces/msg/SurvivorDetectionArray` |
| `/detection/status` | Detection pipeline state | `vayuputra_detection` | `vayuputra_mission`, GCS | `std_msgs/msg/String` |

The `vayuputra_interfaces` package already provides the
`SurvivorDetection` and `SurvivorDetectionArray` interfaces.

---

# 4. ROS 2 Services

## 4.1 Vehicle Services

| Service | Purpose | Client | Server | Interface |
|---|---|---|---|---|
| `/vehicle/arm` | Request vehicle arming | `vayuputra_mission` | `vayuputra_mavlink` | TBD |
| `/vehicle/disarm` | Request vehicle disarming | `vayuputra_mission` | `vayuputra_mavlink` | TBD |
| `/vehicle/set_mode` | Request flight-mode change | `vayuputra_mission` | `vayuputra_mavlink` | TBD |

These services represent the Vayuputra mission layer's interaction with the
PX4/MAVROS flight-control interface.

---

## 4.2 Mission Services

| Service | Purpose | Client | Server | Interface |
|---|---|---|---|---|
| `/mission/start` | Request mission start | GCS / operator | `vayuputra_mission` | TBD |
| `/mission/pause` | Pause the current mission | GCS / operator | `vayuputra_mission` | TBD |
| `/mission/stop` | Stop the current mission | GCS / operator | `vayuputra_mission` | TBD |

These services are architectural decisions for mission management and may be
refined during implementation.

---

# 5. ROS 2 Actions

## 5.1 Navigation Action

### Action

`/navigate_to`

### Purpose

Request autonomous navigation to a specified target pose.

### Goal

- Target position
- Target orientation

### Feedback

- Current pose
- Distance remaining
- Navigation state

### Result

- Success/failure
- Final navigation state

The exact action interface will be finalized during navigation integration.

---

## 5.2 Exploration Action

### Action

`/explore`

### Purpose

Start autonomous indoor exploration using the project's
Hybrid Frontier + Next-Best-View strategy.

### Goal

- Start exploration
- Optional exploration constraints

### Feedback

- Current UAV position
- Exploration progress
- Frontier status
- Current exploration state

### Result

- Exploration completed
- Exploration failed/cancelled

The exact action interface will be finalized during exploration integration.

---

## 5.3 Mission Execution Action

### Action

`/mission/execute`

### Purpose

Execute the complete autonomous search-and-rescue mission.

### Mission Flow

```text
Takeoff
   ↓
Autonomous Exploration
   ↓
Mapping / Localization
   ↓
Survivor Detection
   ↓
Return
   ↓
Land