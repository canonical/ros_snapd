# ros2_snapd

A ROS node to start and stop snap services.

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/ros-snapd)

## Build

This package is distributed as a snap and as such is meant to be built using snapcraft:

```bash
snapcraft --verbose
```

## Use

Using the locally built snap, first install it

```bash
snap install --dangerous ros-snapd*.snap
```

It can also be installed directly from the store:

```bash
snap install ros-snapd
```

The snap automatically starts the node and the services are readily available.

To list available snap service:

```bash
rosservice call /ros_snapd/list
```

To start, stop and restart snap service:

```bash
rosservice call /ros_snapd/start "{service: 'service.name'}"
rosservice call /ros_snapd/stop "{service: 'service.name'}"
rosservice call /ros_snapd/restart "{service: 'service.name'}"
```
