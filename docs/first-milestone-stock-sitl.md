# First milestone: stock PX4 X500 SITL

This is a local record of the first environment bring-up. It intentionally uses
the stock PX4 X500 model; no Vayuputra model, sensor, world, or host ROS 2
files have been added yet.

## Pinned runtime

| Item | Value |
| --- | --- |
| Host | CachyOS (x86_64), Wayland |
| Container image | `px4io/px4-sitl-gazebo-ros2@sha256:f16b9968853ecf37a93301c54fbaaa7363b4d0c50fd7c8a4d8077a8c93f683b1` |
| Container OS | Ubuntu 24.04.4 LTS |
| ROS 2 | Jazzy |
| Gazebo | Gazebo Sim 8.15.0 (Harmonic) |
| PX4/ROS bridge | bundled `MicroXRCEAgent`, UDP 8888 |
| ROS domain | 83 |

The image was verified before use: it contains `/usr/local/bin/MicroXRCEAgent`,
`/usr/local/bin/ros2-entrypoint.sh`, and `/opt/px4-gazebo/bin/px4-gazebo`.

## Reproduce the working baseline

From the repository root:

```bash
scripts/run_stock_sitl.sh
```

The script starts PX4, Gazebo, and the Micro XRCE-DDS Agent inside one named
container on Docker's default bridge network. It does **not** remove an existing
container or make host configuration changes. Inspect the simulation with:

```bash
docker logs --tail 100 vayuputra-px4-bridge
docker exec vayuputra-px4-bridge /usr/local/bin/ros2-entrypoint.sh \
  ros2 topic list
```

PX4's expected ROS topics include `/fmu/in/vehicle_command`,
`/fmu/out/vehicle_local_position`, `/fmu/out/vehicle_status_v4`, and
`/fmu/out/sensor_combined`.

## Flight test commands

The container has no GCS heartbeat. Consequently, normal arming correctly fails
with `Preflight Fail: No connection to the GCS`. Do not treat the following
force-arm sequence as a replacement for a normal GCS-connected test:

```bash
docker exec vayuputra-px4-bridge /bin/bash -lc 'px4-commander arm -f'
docker exec vayuputra-px4-bridge /bin/bash -lc 'px4-commander takeoff'
docker exec vayuputra-px4-bridge /bin/bash -lc 'px4-commander mode auto:land'
```

Inspect state before and after each phase:

```bash
docker exec vayuputra-px4-bridge /bin/bash -lc \
  'px4-commander status; px4-listener vehicle_local_position 1; px4-listener vehicle_land_detected 1'
```

## Evidence recorded on 2026-10-09

- PX4 started the default Gazebo world and spawned the stock X500.
- DDS connected and `ros2 topic list` showed the PX4 `/fmu/in/*` and
  `/fmu/out/*` topics.
- PX4 initially rejected arming only because no GCS was connected.
- A simulation-only force-arm and takeoff succeeded.
- Hover was confirmed in Hold mode at `z = -2.58683 m` (PX4 local NED frame),
  with vertical velocity `-0.01151 m/s`, no failsafe, and airborne land-detector
  state.
- Auto Land was commanded, but its final touchdown/disarm check was interrupted;
  do not mark landing verified until the state check shows `landed: True` and
  `Disarmed`.

## Important host networking finding

`--network host` is not usable for this Gazebo setup on this CachyOS host:
Gazebo Transport logged `Exception sending a multicast message: Network is
unreachable`, and PX4 timed out waiting for a world. Docker's default bridge
network fixed discovery because PX4, Gazebo, and the Agent are co-located in one
container. Keep that arrangement for the first milestone.

## Next step

Add a GCS heartbeat path (QGroundControl or a minimal MAVLink test client) and
repeat takeoff, hover, landing, and disarm without force arming. Only then
commit this first milestone and begin the Vayuputra vehicle model work.
