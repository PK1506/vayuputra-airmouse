# Vayuputra ROS 2 Communication Specification

## 1. Purpose

This document defines the ROS 2 communication architecture and interfaces for the Vayuputra AirMouse system.

The architecture connects:

- Sensors
- SLAM and localization
- Navigation
- Autonomous exploration
- Survivor detection
- Mission management
- MAVROS / PX4 integration
- Ground Control Station (GCS)

The system is intended to support GPS-denied indoor autonomous search and rescue.

This document distinguishes implemented software foundations from proposed interfaces and integrations that remain to be completed. An interface definition or configuration file does not, by itself, mean that the corresponding live data pipeline or algorithm is operational.

---

## 2. Communication Model

Vayuputra uses three main ROS 2 communication mechanisms.

### 2.1 Topics

Topics carry continuous or streaming data, including:

- Sensor measurements
- Robot pose and odometry
- Maps
- Detection results
- Navigation state
- Exploration state

### 2.2 Services

Services handle short request/response operations, including:

- Vehicle arming and disarming
- Flight-mode requests
- Mission start, pause and stop requests

### 2.3 Actions

Actions support long-running operations that require feedback and a final result, including:

- Navigation to a target
- Autonomous exploration
- Complete mission execution

The custom mission execution action is defined in this project, but its action server and end-to-end execution logic remain to be implemented.

---

# 3. ROS 2 Topics

## 3.1 Sensor Topics

| Topic | Purpose | Intended Publisher | Intended Subscriber | Message Type |
|---|---|---|---|---|
| `/sensors/lidar/points` | LiDAR point cloud | `vayuputra_sensors` / sensor driver | `vayuputra_slam` | `sensor_msgs/msg/PointCloud2` |
| `/sensors/depth/image` | Depth camera image | `vayuputra_sensors` / camera driver | `vayuputra_slam`, `vayuputra_detection` | `sensor_msgs/msg/Image` |
| `/sensors/camera/image` | RGB camera image | `vayuputra_sensors` / camera driver | `vayuputra_detection` | `sensor_msgs/msg/Image` |
| `/sensors/camera/camera_info` | Camera calibration data | `vayuputra_sensors` / camera driver | `vayuputra_detection` | `sensor_msgs/msg/CameraInfo` |
| `/sensors/imu/data` | IMU measurements | `vayuputra_sensors` / MAVROS | `vayuputra_slam` | `sensor_msgs/msg/Imu` |

### Sensor Interface Requirements

Vayuputra reuses standard ROS 2 sensor messages instead of defining duplicate sensor data types.

| Sensor | Message Type | Purpose |
|---|---|---|
| LiDAR | `sensor_msgs/msg/PointCloud2` | 3D point-cloud data |
| Depth camera | `sensor_msgs/msg/Image` | Depth image data |
| RGB camera | `sensor_msgs/msg/Image` | Camera image data |
| Camera calibration | `sensor_msgs/msg/CameraInfo` | Camera intrinsics and calibration |
| IMU | `sensor_msgs/msg/Imu` | Orientation, angular velocity and linear acceleration |

The `vayuputra_sensors` package currently provides topic configuration through YAML and a configuration node. These components declare and report configured topic names and message types; they do not establish that the physical sensor drivers are publishing live data.

Sensor publishers must provide appropriate timestamps and coordinate frame IDs. Sensor frame names must match the TF2 structure documented in `docs/tf2_frames.md`.

The exact topic names may need to be adapted to the selected drivers during integration.

---

## 3.2 SLAM and Localization Topics

| Topic | Purpose | Intended Publisher | Intended Subscriber | Message Type |
|---|---|---|---|---|
| `/slam/map` | 2D occupancy-grid map | `vayuputra_slam` | `vayuputra_navigation`, `vayuputra_exploration`, GCS | `nav_msgs/msg/OccupancyGrid` |
| `/slam/pose` | Estimated UAV pose | `vayuputra_slam` | `vayuputra_navigation`, `vayuputra_mission` | `geometry_msgs/msg/PoseStamped` |
| `/slam/odometry` | Estimated UAV motion | `vayuputra_slam` | `vayuputra_navigation`, `vayuputra_mission` | `nav_msgs/msg/Odometry` |

### SLAM Interface Requirements

- The map publisher must provide valid resolution, dimensions, origin and occupancy data.
- Pose and odometry messages must use consistent coordinate frames and timestamps.
- The SLAM implementation must publish the appropriate TF2 transforms when configured to do so.
- The final topics must be compatible with the selected SLAM implementation.

The `vayuputra_slam` package currently includes topic configuration and a configuration node. The node reports the configured topic names and message types; it does not implement a SLAM algorithm or publish a live map, pose or odometry.

The topic names are proposed project-level names. Remapping may be required when integrating a third-party SLAM package.

---

## 3.3 Navigation Topics

| Topic | Purpose | Intended Publisher | Intended Subscriber | Message Type |
|---|---|---|---|---|
| `/navigation/goal` | Requested navigation target | `vayuputra_exploration` / `vayuputra_mission` | `vayuputra_navigation` | `geometry_msgs/msg/PoseStamped` |
| `/navigation/cmd_vel` | Navigation velocity command | `vayuputra_navigation` | Flight-control adapter | `geometry_msgs/msg/Twist` |
| `/navigation/status` | Current navigation state | `vayuputra_navigation` | `vayuputra_mission`, GCS | `std_msgs/msg/String` |

### Navigation Interface Requirements

- Navigation goals must specify a valid coordinate frame.
- Navigation status must use documented state values.
- Velocity commands must be translated into the command interface expected by the flight-control layer.
- The navigation implementation must respect configured vehicle-control limits and failsafe behavior.

The `vayuputra_navigation` package currently includes topic configuration and a configuration node. The node reports configured topic names and message types; it does not implement path planning, goal execution or live velocity-command publication.

`geometry_msgs/msg/Twist` is a proposed project-level command type. Compatibility with the selected PX4/MAVROS control interface must be verified during integration.

---

## 3.4 Exploration Topics

| Topic | Purpose | Intended Publisher | Intended Subscriber | Message Type |
|---|---|---|---|---|
| `/exploration/frontiers` | Detected unexplored map regions | `vayuputra_exploration` | `vayuputra_exploration`, GCS | TBD |
| `/exploration/next_best_view` | Selected next-best-view target | `vayuputra_exploration` | `vayuputra_navigation` | `geometry_msgs/msg/PoseStamped` |
| `/exploration/status` | Exploration state and progress | `vayuputra_exploration` | `vayuputra_mission`, GCS | `std_msgs/msg/String` |

### Exploration Interface Requirements

- The frontier representation must be selected when the exploration algorithm is implemented.
- Next-best-view targets must use a valid coordinate frame.
- Exploration status should indicate whether exploration is idle, active, completed or failed.
- The Hybrid Frontier + Next-Best-View strategy must integrate with the selected SLAM and navigation implementations.

The frontier message type remains TBD until the algorithm's data requirements are finalized.

---

## 3.5 Survivor Detection Topics

| Topic | Purpose | Intended Publisher | Intended Subscriber | Message Type |
|---|---|---|---|---|
| `/detection/survivors` | Detected survivor information | `vayuputra_detection` | `vayuputra_mission`, GCS | `vayuputra_interfaces/msg/SurvivorDetectionArray` |
| `/detection/status` | Detection pipeline state | `vayuputra_detection` | `vayuputra_mission`, GCS | `std_msgs/msg/String` |

The `vayuputra_interfaces` package defines these custom messages:

- `SurvivorDetection`
- `SurvivorDetectionArray`

### Survivor Detection Interface Requirements

- Detection confidence must be represented consistently between 0.0 and 1.0.
- Detection coordinates must identify the coordinate frame used for the position.
- If a valid 3D position is unavailable, `has_position` must be false.
- Detection timestamps and coordinate frames must be consistent with the containing array header.
- Bounding-box coordinates must use the source image's pixel coordinate system.

The message definitions are available, but a complete detection pipeline and live topic publishers must be verified separately.

---

# 4. ROS 2 Services

## 4.1 Vehicle Services

| Proposed Service | Purpose | Client | Intended Server | Interface |
|---|---|---|---|---|
| `/vehicle/arm` | Request vehicle arming | `vayuputra_mission` | `vayuputra_mavlink` | TBD |
| `/vehicle/disarm` | Request vehicle disarming | `vayuputra_mission` | `vayuputra_mavlink` | TBD |
| `/vehicle/set_mode` | Request flight-mode change | `vayuputra_mission` | `vayuputra_mavlink` | TBD |

These are proposed Vayuputra-level service names. The `vayuputra_mavlink` package is responsible for translating mission-level requests into the appropriate MAVROS/PX4 interfaces.

### Vehicle Service Requirements

- Service responses must indicate whether a request was accepted or failed.
- A successful service response must not be treated as proof that the vehicle reached the requested state.
- The implementation must verify actual vehicle state through appropriate telemetry.
- Arming, disarming and mode changes must respect PX4 safety checks and configured failsafes.

Standard MAVROS interfaces include:

- `mavros_msgs/srv/CommandBool` for arming/disarming requests.
- `mavros_msgs/srv/SetMode` for flight-mode requests.

These interfaces should be reused where appropriate rather than duplicated unnecessarily.

**Status:** The vehicle services are documented as proposed interfaces. Their implementation and PX4/MAVROS integration remain pending verification.

---

## 4.2 Mission Services

| Service | Purpose | Client | Server | Interface |
|---|---|---|---|---|
| `/mission/command` | Request mission start, pause or stop | GCS / operator / mission client | `vayuputra_mission` | `vayuputra_interfaces/srv/MissionCommand` |

### MissionCommand Service Definition

The custom service contains the following fields.

**Request**

- `mission_id`: Identifier of the mission.
- `command`: Requested command, currently supporting `start`, `pause` or `stop`.

**Response**

- `accepted`: Whether the request was accepted.
- `message`: Human-readable response.

### Current Implementation

The `vayuputra_mission` package provides a `mission_manager_node` service server at `/mission/command`.

The current implementation maintains an in-memory mission state and supports basic start, pause and stop requests.

The service has been tested with ROS 2 service calls.

The current implementation does not execute the complete search-and-rescue mission, invoke Nav2, perform vehicle-control operations or persist mission state across node restarts.

Mission validation, persistent state, safe-stop behavior and integration with other modules remain future work.

---

# 5. ROS 2 Actions

## 5.1 Navigation Action

### Action Name

`/navigate_to`

### Intended Purpose

Request autonomous navigation to a specified target pose.

### Proposed Goal

- Target pose
- Optional navigation constraints

### Proposed Feedback

- Current pose
- Distance remaining
- Navigation state

### Proposed Result

- Success or failure
- Final navigation state
- Optional failure information

### Implementation Note

The standard Nav2 action `nav2_msgs/action/NavigateToPose` should be evaluated and reused where compatible with the Vayuputra navigation architecture.

The navigation configuration currently records `/navigate_to` and the standard Nav2 action type. This configuration does not itself create an action server or execute navigation goals.

A custom navigation action should only be introduced if the standard interface does not meet project requirements.

---

## 5.2 Exploration Action

### Action Name

`/explore`

### Intended Purpose

Start autonomous indoor exploration using the Hybrid Frontier + Next-Best-View strategy.

### Proposed Goal

- Exploration request
- Optional exploration constraints

### Proposed Feedback

- Current UAV position
- Exploration progress
- Frontier status
- Current exploration state

### Proposed Result

- Exploration completed or failed
- Final exploration state
- Optional failure information

### Implementation Note

The exact action interface must be finalized based on the exploration algorithm and mission-management requirements.

The exploration action server and algorithm remain to be implemented and tested.

---

## 5.3 Mission Execution Action

### Intended Action Name

`/mission/execute`

### Custom Interface

`vayuputra_interfaces/action/ExecuteMission`

### Intended Purpose

Execute the complete autonomous search-and-rescue mission.

### Goal Fields

- `mission_id`
- `mission_config`

### Feedback Fields

- `current_stage`
- `progress`

### Result Fields

- `success`
- `message`

### Proposed Mission Flow

```text
Mission Start
     |
     v
Vehicle Readiness Checks
     |
     v
Takeoff
     |
     v
Autonomous Exploration
     |
     v
Mapping and Localization
     |
     v
Survivor Detection
     |
     v
Return to Designated Location
     |
     v
Landing
     |
     v
Mission Complete
```

The actual mission sequence, transition conditions and failure handling must be finalized with the mission-management and flight-control teams.

The custom `ExecuteMission.action` interface has been defined and generated by the ROS 2 build system. An action server, feedback publication, result handling and end-to-end mission execution remain to be implemented.

Long-running mission execution should use an action so that clients can receive feedback and observe the final result.

---

# 6. TF2 Coordinate Frame Requirements

The proposed TF2 hierarchy is documented in `docs/tf2_frames.md`.

```text
map
└── odom
    └── base_link
        ├── lidar_link
        ├── camera_link
        │   └── camera_depth_frame
        └── imu_link
```

### Frame Requirements

- `map` represents the global mapping frame.
- `odom` represents the local odometry frame.
- `base_link` represents the UAV body frame.
- `lidar_link` represents the LiDAR sensor frame.
- `camera_link` represents the camera frame.
- `camera_depth_frame` represents the depth camera frame.
- `imu_link` represents the IMU frame.

### Current Implementation

A static TF2 launch file has been created and included in the common bringup launch structure.

The current static sensor transforms use placeholder translation and rotation values. These values are not calibrated and must not be treated as final sensor extrinsics.

The `map -> odom` and `odom -> base_link` transforms are expected to be provided by the appropriate SLAM, localization or state-estimation components.

The final frame names, transform ownership and calibrated sensor transforms must be verified against the selected drivers and state-estimation implementation.

---

# 7. Interface Ownership

| Package | Responsibility | Current Foundation Status |
|---|---|---|
| `vayuputra_bringup` | Common launch files and system startup | Common bringup and TF2 launch structure created |
| `vayuputra_interfaces` | Shared custom messages, services and actions | Detection messages, `MissionCommand` service and `ExecuteMission` action defined |
| `vayuputra_sensors` | Sensor data integration and sensor topic publication | Topic configuration and configuration node created; physical sensor integration pending |
| `vayuputra_slam` | Mapping, localization and estimated pose | Topic configuration and configuration node created; actual SLAM implementation pending |
| `vayuputra_navigation` | Navigation goals, path execution and velocity commands | Topic/action configuration and configuration node created; actual navigation execution pending |
| `vayuputra_exploration` | Frontier detection and next-best-view selection | Package exists; complete interface and algorithm verification pending |
| `vayuputra_detection` | Survivor detection and detection status | Package exists; complete pipeline verification pending |
| `vayuputra_mission` | Mission state, mission control and mission execution | Basic mission command service implemented; full mission execution pending |
| `vayuputra_mavlink` | MAVROS/PX4 communication and vehicle-control adapters | Package exists; live vehicle integration and verification pending |

These responsibilities describe the proposed package architecture. Actual publishers, subscribers, service servers and action servers must be verified during integration.

---

# 8. Interface Design Rules

1. Reuse standard ROS 2 messages, services and actions whenever they meet project requirements.
2. Define custom interfaces only when project-specific data or behavior requires them.
3. Use consistent topic and interface names across packages.
4. Populate timestamps and coordinate frame IDs where applicable.
5. Document QoS settings for sensor streams and other topics where compatibility matters.
6. Document status values and failure responses.
7. Avoid duplicating standard interfaces unnecessarily.
8. Verify interfaces against the selected sensor drivers, SLAM package, Nav2 configuration and MAVROS/PX4 integration.
9. Do not treat a successful request response as proof that a long-running operation has completed.
10. Update this document whenever an interface changes.
11. Distinguish configuration nodes from actual data-processing and control nodes.
12. Do not mark a component as operational until its behavior has been tested.

---

# 9. Implementation Status

| Component | Status | Notes |
|---|---|---|
| ROS 2 package structure | Created | Nine project packages are discoverable in the workspace |
| Standard sensor message types | Identified | Standard ROS 2 messages reused |
| Sensor topic configuration | Implemented | YAML and configuration node created |
| Physical sensor drivers | Pending | Live LiDAR, camera and IMU integration must be tested |
| SLAM topic configuration | Implemented | YAML and configuration node created |
| SLAM algorithm and publishers | Pending | No live map, pose or odometry pipeline established by the configuration node |
| Navigation topic configuration | Implemented | YAML and configuration node created |
| Nav2 goal execution | Pending | Actual action-server behavior must be tested |
| Exploration interface | Partially specified | Frontier message type remains TBD |
| Survivor detection messages | Defined | Custom messages created and generated |
| Complete detection pipeline | Pending verification | Live detection publishers and subscribers must be tested |
| `MissionCommand` service | Implemented | `/mission/command` tested with start, pause and stop requests |
| `ExecuteMission.action` | Defined | Action server and execution logic pending |
| Vehicle service architecture | Documented | Project-level service implementation pending |
| PX4/MAVROS integration | Pending verification | Live telemetry and vehicle-control interfaces must be tested |
| TF2 frame structure | Documented | Static sensor transforms use placeholders |
| Common bringup launch files | Created | Launch behavior must be validated with integrated components |
| Full end-to-end mission | Pending | Requires integration and system-level testing |

---

# 10. Testing and Integration Checklist

Before a component is considered integration-ready:

- [ ] Confirm its ROS 2 package builds successfully.
- [ ] Confirm its launch files start correctly.
- [ ] Verify topic names and message types.
- [ ] Verify that expected publishers and subscribers are actually active.
- [ ] Verify timestamps and coordinate frame IDs.
- [ ] Confirm QoS compatibility where applicable.
- [ ] Test service requests and responses.
- [ ] Test action goals, feedback, cancellation and results where applicable.
- [ ] Validate TF2 transforms using calibrated values.
- [ ] Verify failure handling and failsafe behavior.
- [ ] Test integration with dependent packages.
- [ ] Update the documentation with the test results.

---

# 11. Conclusion

This document is the initial ROS 2 communication specification for the Vayuputra AirMouse project.

The current foundation includes ROS 2 packages, custom detection messages, a mission command service, a mission execution action definition, sensor/SLAM/navigation topic configuration nodes and a static TF2 launch structure.

These components establish a foundation for integration but do not, by themselves, constitute a complete autonomous search-and-rescue system.

Interfaces marked as proposed, TBD or pending must be finalized, implemented and tested before their associated components are considered operational.