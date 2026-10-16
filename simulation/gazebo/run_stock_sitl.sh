#!/usr/bin/env bash
set -euo pipefail

# Reproducible stock PX4 + Gazebo Harmonic + ROS 2 Jazzy baseline.
# This deliberately uses Docker's default bridge network. Host networking caused
# Gazebo Transport multicast failures on the CachyOS development host.
IMAGE='px4io/px4-sitl-gazebo-ros2@sha256:f16b9968853ecf37a93301c54fbaaa7363b4d0c50fd7c8a4d8077a8c93f683b1'
CONTAINER='vayuputra-px4-bridge'

if ! docker info >/dev/null 2>&1; then
  echo 'Docker daemon is unavailable. Start Docker and ensure this user can access it.' >&2
  exit 1
fi

if docker container inspect "$CONTAINER" >/dev/null 2>&1; then
  echo "Container '$CONTAINER' already exists; inspect or remove it explicitly before starting a new run." >&2
  exit 1
fi

docker run -d \
  --name "$CONTAINER" \
  -e HEADLESS=1 \
  -e ROS_DOMAIN_ID=83 \
  "$IMAGE" \
  /bin/bash -lc 'MicroXRCEAgent udp4 -p 8888 > /tmp/microxrce-agent.log 2>&1 & exec px4-gazebo'

echo "Started $CONTAINER."
echo "Follow PX4 with: docker logs --tail 100 -f $CONTAINER"
echo "List ROS topics with: docker exec $CONTAINER /usr/local/bin/ros2-entrypoint.sh ros2 topic list"
