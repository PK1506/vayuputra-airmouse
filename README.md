# Vayuputra - NIDAR AirMouse

Vayuputra is an indoor UAV search-and-rescue project targeting GPS-denied
operation. The intended flight stack is PX4 with ROS 2 Jazzy, simulation in
Gazebo, mapping and navigation in ROS 2, and a React/FastAPI ground control
station.

## Repository status

The repository is at its initial implementation stage. The ROS 2 workspace
currently contains `vayuputra_interfaces`, which defines the first
perception-to-mapping/GCS message contract. PX4 integration, simulation,
sensors, SLAM, navigation, exploration, mission management, detection nodes,
and the ground control station have not been implemented yet.

```text
ros2_ws/
└── src/
    └── vayuputra_interfaces/   # Shared ROS 2 message definitions
```

Keep simulation assets separate from real-hardware configuration. ROS
functionality should be split into focused packages as those components are
implemented rather than placing the system in one monolithic package.

## Prerequisites

- Ubuntu 24.04
- ROS 2 Jazzy
- `colcon` and the ROS 2 `rosidl` build tools

The ROS workspace has not yet been validated on Windows.

## Build the ROS 2 interfaces

From the repository root in a ROS 2 Jazzy environment:

```bash
source /opt/ros/jazzy/setup.bash
cd ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

The generated message types are provided by the `vayuputra_interfaces`
package. For example:

```bash
ros2 interface show vayuputra_interfaces/msg/SurvivorDetectionArray
```

## Planned implementation sequence

1. Add bringup and configuration once the component launch contracts are
   defined.
2. Add Gazebo/PX4 SITL integration and verify a simulated vehicle connection.
3. Add sensor drivers and ROS integration, then SLAM/localization and map
   outputs.
4. Implement navigation, exploration, obstacle handling, and mission
   management as separate ROS 2 packages.
5. Add survivor detection and depth-based map positioning using the shared
   interfaces.
6. Add the FastAPI/MAVSDK backend and React GCS, then validate the full flow in
   SITL before targeting hardware.

Each component should include its own build/run instructions and tests as it
is added. Hardware behavior must not be considered verified based on SITL
results alone.
