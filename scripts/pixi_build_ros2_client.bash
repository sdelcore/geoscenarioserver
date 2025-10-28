#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR=$(dirname "$SCRIPT_DIR")
mkdir -p ${REPO_DIR}/colcon_ws/src
ln -sfn ${REPO_DIR}/clients/ros2_clients ${REPO_DIR}/colcon_ws/src/clients
ln -sfn ${REPO_DIR}/ros ${REPO_DIR}/colcon_ws/src/ros
cd ${REPO_DIR}/colcon_ws
colcon build $@
