# NIDAR AirMouse — ROS 2 SLAM Integration Documentation

## 1. Objective

The objective of this integration is to simulate an indoor drone using PX4 and Gazebo, obtain LiDAR and odometry data through ROS 2, generate a live 2D occupancy grid using SLAM Toolbox, and visualize the mapping process in RViz2.

The setup was tested by moving the simulated drone through the environment and confirming that the map updated in RViz2.

## 2. Software and Dependencies

The following software components are used in the current setup.

| Component | Purpose |
|---|---|
| Ubuntu 24.04 LTS | Operating system |
| ROS 2 Jazzy | Robot communication and integration |
| PX4 Autopilot | Drone flight-control software and state estimation |
| Gazebo | Drone and environment simulation |
| `ros_gz_bridge` | Transfers supported sensor messages between Gazebo and ROS 2 |
| SLAM Toolbox | Generates a 2D map from LiDAR and odometry/TF |
| RViz2 | Visualizes the map, LiDAR data, and TF frames |
| `px4_msgs` | ROS 2 message definitions for PX4 |
| `nav2_map_server` | Saves the generated occupancy grid to files |

### Workspace locations

- PX4 repository: `~/PX4-Autopilot`
- PX4 ROS 2 workspace: `~/ros2_px4_ws`
- NIDAR project workspace: `~/vayuputra-airmouse/ros2_ws`
- Configuration directory: `~/vayuputra-airmouse/config`
- Saved maps directory: `~/vayuputra-airmouse/maps`

## 3. Launching PX4 and Gazebo

Open a terminal and run:

```bash
cd ~/PX4-Autopilot
PX4_GZ_WORLD=airmouse_map make px4_sitl gz_x500_lidar_2d
```

**Purpose:**
- Starts PX4 Software-in-the-Loop (SITL).
- Launches the X500 drone model with the configured 2D LiDAR sensor.
- Loads the `airmouse_map` Gazebo world.

Keep this terminal running while testing the other components.

## 4. Starting the Static TF Publisher

Open another terminal and run:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_px4_ws/install/setup.bash
source ~/vayuputra-airmouse/ros2_ws/install/setup.bash

ros2 launch vayuputra_bringup tf2_static.launch.py
```

**Purpose:** Publishes the configured static transforms between the robot's base frame and its sensor-related frames.

The configured transforms include:

- `base_link → link`
- `base_link → camera_link`
- `base_link → imu_link`
- `camera_link → camera_depth_frame`

The camera and IMU transforms currently use identity transforms, so their physical alignment should be validated before relying on them for real hardware.

## 5. Connecting Gazebo LiDAR to ROS 2

Open another terminal and run:

```bash
source /opt/ros/jazzy/setup.bash

ros2 run ros_gz_bridge parameter_bridge \
'/world/airmouse_map/model/x500_lidar_2d_0/link/link/sensor/lidar_2d_v2/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan' \
--ros-args \
-r /world/airmouse_map/model/x500_lidar_2d_0/link/link/sensor/lidar_2d_v2/scan:=/scan \
-p override_timestamps_with_wall_time:=true
```

**Purpose:**
- Bridges the Gazebo LiDAR scan into ROS 2.
- Publishes the scan on `/scan`.
- Uses wall-clock timestamps for the bridged scan messages.

The LiDAR topic was observed publishing at approximately 30 Hz in the tested setup.

The Gazebo topic path depends on the world and spawned model configuration. If the model name or sensor configuration changes, this path may need to be updated.

## 6. Connecting PX4 Odometry to ROS 2

The PX4 odometry topic used in this setup is:

`/fmu/out/vehicle_odometry`

Message type:

`px4_msgs/msg/VehicleOdometry`

Run the odometry converter in another terminal:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_px4_ws/install/setup.bash
source ~/vayuputra-airmouse/ros2_ws/install/setup.bash

ros2 run vayuputra_mavlink odometry_converter
```

**Purpose:**
- Converts PX4 odometry messages into ROS 2 odometry messages.
- Publishes `/odom` using `nav_msgs/msg/Odometry`.
- Publishes the `odom → base_link` transform.

The odometry and TF data provide the robot-pose information required by the SLAM pipeline.

Coordinate-frame conversion and odometry accuracy should be validated before using this configuration on a physical drone.

## 7. Publishing IMU Data

The source PX4 topic is:

`/fmu/out/sensor_combined`

Run the IMU converter:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_px4_ws/install/setup.bash
source ~/vayuputra-airmouse/ros2_ws/install/setup.bash

ros2 run vayuputra_mavlink imu_converter
```

The converted IMU topic is:

`/sensors/imu/data`

Message type:

`sensor_msgs/msg/Imu`

The converted topic was observed publishing at approximately 249 Hz.

**Important:** The IMU converter makes IMU data available in ROS 2, but the current SLAM Toolbox configuration does not directly consume this IMU topic. The working mapping pipeline uses LiDAR, odometry, and TF.

## 8. SLAM Toolbox Configuration

The SLAM parameters are stored in:

`~/vayuputra-airmouse/config/slam_params.yaml`

The relevant configured parameters are:

| Parameter | Value |
|---|---|
| `map_frame` | `map` |
| `odom_frame` | `odom` |
| `base_frame` | `base_link` |
| `scan_topic` | `/scan` |
| `use_sim_time` | `false` |

Launch SLAM Toolbox in another terminal:

```bash
source /opt/ros/jazzy/setup.bash

ros2 launch slam_toolbox online_async_launch.py \
slam_params_file:=/home/rahul-ubuntu/vayuputra-airmouse/config/slam_params.yaml \
use_sim_time:=false
```

Replace `/home/rahul-ubuntu` if the configuration file is stored under a different Linux home directory.

**Purpose:** SLAM Toolbox processes LiDAR scans together with the configured odometry and TF information to build a live 2D occupancy grid.

## 9. Visualizing the Map in RViz2

Open another terminal:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_px4_ws/install/setup.bash
source ~/vayuputra-airmouse/ros2_ws/install/setup.bash

rviz2
```

Configure RViz2 as follows:

1. Set **Fixed Frame** to `map`.
2. Add a **Map** display and select `/map`.
3. Add a **LaserScan** display and select `/scan`.
4. Add a **TF** display to inspect the coordinate frames.

### Expected TF structure

```text
map
 └── odom
      └── base_link
           ├── link
           ├── camera_link
           │    └── camera_depth_frame
           └── imu_link
```

`map → odom` is provided by the SLAM system, while `odom → base_link` is published by the odometry converter.

The tree above represents the configured and observed TF structure. Sensor mounting offsets and frame orientations still require validation for real hardware.

## 10. ROS 2 Topics

| Topic | Message type | Purpose |
|---|---|---|
| `/scan` | `sensor_msgs/msg/LaserScan` | LiDAR scans bridged from Gazebo |
| `/fmu/out/vehicle_odometry` | `px4_msgs/msg/VehicleOdometry` | PX4 vehicle odometry |
| `/odom` | `nav_msgs/msg/Odometry` | Converted odometry for ROS 2 |
| `/fmu/out/sensor_combined` | `px4_msgs/msg/SensorCombined` | PX4 combined sensor data |
| `/sensors/imu/data` | `sensor_msgs/msg/Imu` | Converted IMU data |
| `/map` | `nav_msgs/msg/OccupancyGrid` | Live occupancy grid from SLAM Toolbox |

The listed topics describe the current configuration. Exact availability depends on which publishers and launch processes are running.

## 11. Saving the Generated Map

Create the maps directory and save the map:

```bash
mkdir -p ~/vayuputra-airmouse/maps

ros2 run nav2_map_server map_saver_cli \
-f ~/vayuputra-airmouse/maps/nidar_map
```

The generated files are:

- `~/vayuputra-airmouse/maps/nidar_map.pgm`
- `~/vayuputra-airmouse/maps/nidar_map.yaml`

The PGM file stores the occupancy-grid image, while the YAML file stores map metadata such as resolution and origin.

The map was saved successfully. Its reported dimensions were approximately **8262 × 8736 pixels at 0.05 m/pixel**. This is a relatively large map and should be reviewed for mapping-area size and odometry accuracy before treating it as a final environment map.

## 12. Verification and Testing

The following tests were completed:

- PX4 and Gazebo simulation launched.
- LiDAR data was bridged to the ROS 2 `/scan` topic.
- PX4 odometry was converted to `/odom`.
- The TF tree was connected and visualized.
- SLAM Toolbox generated a live occupancy grid.
- RViz2 displayed the map and LiDAR data.
- The simulated drone was moved through the environment.
- The map updated during movement.
- The occupancy grid was saved to PGM and YAML files.
- The IMU converter published `/sensors/imu/data`.

### Test result

**Result: Successful simulation mapping test.**

The simulated platform's movement produced updates to the live map in RViz2, and the generated map was saved successfully.

## 13. Known Limitations

1. **Simulation only:** The current result demonstrates the simulation pipeline, not a validated real-drone deployment.
2. **IMU integration:** IMU data is published to ROS 2 but is not directly used by the current SLAM Toolbox configuration.
3. **Coordinate frames:** Camera and IMU static transforms currently use identity transforms and need physical calibration for real hardware.
4. **Odometry validation:** PX4-to-ROS coordinate conversion and odometry accuracy require further testing.
5. **Map size:** The saved map is large; its dimensions and mapped area should be reviewed.
6. **Clock configuration:** The LiDAR bridge uses wall-clock timestamps, and SLAM Toolbox is configured with `use_sim_time:=false`. These settings should remain consistent with the running simulation and TF timestamps.
7. **Environment-specific topic path:** The Gazebo LiDAR topic path depends on the world, model, and sensor names.
8. **No real-flight validation:** Mapping accuracy, sensor alignment, and safety have not been validated on physical hardware.

## 14. Summary

The NIDAR AirMouse simulation pipeline connects PX4 and Gazebo with ROS 2, bridges LiDAR scans, converts PX4 odometry, and uses SLAM Toolbox to generate a live 2D occupancy grid. RViz2 provides visualization, and the generated map can be saved for later use.

The simulation mapping test was completed successfully. Further work should focus on validating coordinate conversions, checking the saved map's size and quality, and preparing the pipeline for later integration and testing.