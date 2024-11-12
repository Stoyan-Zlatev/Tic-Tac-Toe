#!/bin/bash

# Allow Docker to connect to the X server (for Linux)
xhost +local:docker

# Run the Docker container with display settings for GUI applications
sudo docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    tic-tac-toe-game

# Revoke access to the X server after the container stops
xhost -local:docker
