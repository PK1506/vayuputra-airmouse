# PX4 SITL Arming & Sensor Integration

## Objective

Verify the Gazebo → PX4 SITL sensor and arming workflow for the AirMouse simulation.

Workflow:

Gazebo → Magnetometer → GZBridge → PX4 → Heading Estimation → Arming → Takeoff

## Problem Identified

The custom `airmouse_map.sdf` Gazebo world was missing the required `spherical_coordinates` configuration.

This resulted in the PX4 SITL simulation showing magnetic/no-heading pre-arm issues.

## Fix

- Added the required `spherical_coordinates` configuration to `airmouse_map.sdf`.
- Verified the existing PX4 GZBridge magnetometer conversion.
- Adjusted the simulated magnetometer noise configuration.
- Rebuilt PX4 successfully.

## Verification

The following were successfully verified:

- PX4 pre-flight checks passed.
- PX4 vehicle status was received through ROS 2.
- IMU data was received from `/fmu/out/sensor_combined`.
- Magnetometer data was received from PX4.
- PX4 SITL successfully armed.
- The simulated vehicle successfully took off.
- Stable hover was achieved in the custom AirMouse Gazebo world.

## ROS 2 Topics Verified

- `/fmu/out/vehicle_status_v4`
- `/fmu/out/sensor_combined`
- `/fmu/out/vehicle_attitude`
- `/fmu/out/vehicle_local_position_v1`

## Vehicle Status Verification

The following were verified:

- `pre_flight_checks_pass: true`
- `failsafe: false`
- `gcs_connection_lost: false`
- `safety_off: true`

## Test Evidence

Evidence collected during testing:

1. PX4 vehicle status screenshot
2. IMU sensor data screenshot
3. Magnetometer data screenshot
4. Successful SITL takeoff and stable-hover video

## Result

PX4 SITL sensor verification, pre-flight checks, arming, takeoff, and stable hover were successfully demonstrated in the custom AirMouse Gazebo environment.

## Simulation Asset

Tested Gazebo world:

`simulation/worlds/airmouse_map.sdf`

## Status

Technical implementation and simulation testing completed.

GitHub Pull Request and Issue update remain pending.
