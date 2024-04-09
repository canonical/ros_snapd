# ros2_snapd

A ROS 2 node to start and stop snap services.

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/ros2-snapd)

## Build

This package is distributed as a snap and as such is meant to be built using snapcraft:

```bash
snapcraft --verbose
```

## Use

Using the locally built snap, first install it

```bash
snap install --dangerous ros2-snapd*.snap
```

It can also be installed directly from the store:

```bash
snap install ros2-snapd
```

The snap automatically starts the node and the services are readily available.

To list available snap service:

```bash
ros2 service call /ros2_snapd/list ros2_snapd/srv/SnapdList
```

To start, stop and restart snap service:

```bash
ros2 service call /ros2_snapd/start ros2_snapd/srv/SnapdStart "service: 'service.name'"
ros2 service call /ros2_snapd/stop ros2_snapd/srv/SnapdStop "service: 'service.name'"
ros2 service call /ros2_snapd/restart ros2_snapd/srv/SnapdRestart "service: 'service.name'"
```
