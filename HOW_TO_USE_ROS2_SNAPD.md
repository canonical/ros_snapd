# How to use ros2-snapd

For this 'how to' guide we will use the `ros2-snapd` to run 
[nav2](https://navigation.ros.org/) SLAM on the [Husarion ROSbot XL](https://husarion.com/manuals/rosbot-xl/).

We use Ubuntu 22.04 and the corresponding ROS 2 Humble distribution.

Before starting this how to guide, make sure to follow the 
official [instructions to build and run ROSbot XL simulation](https://github.com/husarion/rosbot_xl_ros?tab=readme-ov-file#build-and-run-gazebo-simulation).


## Install the snaps

First install the `ros2-snapd` snap:

```
sudo snap install ros2-snapd
```

Also, make sure to install ros2-nav2:

```
sudo snap install ros2-nav2
```

Then, configure the ros2-nav2 with some default configuration:

```
sudo snap set ros2-nav2 slam-config=/var/snap/ros2-nav2/common/configuration_templates/slam_params_template.yaml
```

### Install the `ros_snapd_interfaces`

In another terminal, install `ros2-snapd` interfaces:

```
sudo apt install ros-jazzy-ros-snapd-interfaces
```

## Start and stop the ros2-nav.slam

First, make sure to start the simulation:

```
ros2 launch rosbot_xl_gazebo simulation.launch.py
```

### List the available snapd services

Here we use `ros2-snapd` to list the available
snap services that we can interract with.

```
ros2 service call /ros2_snapd/list ros_snapd_interfaces/srv/SnapdList
```

This returns a list containing `ros2-nav2.slam` among other services.

### Start the `ros2-nav2.slam` service from ROS 2

Now, we use the `ros2-snapd` to start our SLAM.
Using the snap CLI we would issue: `sudo snap start ros2-nav2.slam`.
With `ros2-snapd`, we can start the service from a ROS service:

```
ros2 service call /ros2_snapd/start ros_snapd_interfaces/srv/SnapdStart "service: 'ros2-nav2.slam'"
```

We can verify that our service is started with:

```
snap info ros2-nav2
```

### Stop the `ros2-nav2.slam` service from ROS 2 

Finally, we use the `ros2-snapd` to stop our SLAM.
Using the snap CLI we would issue: `sudo snap stop ros2-nav2.slam`.
With `ros2-snapd`, we can stop the service from a ROS service:

```
ros2 service call /ros2_snapd/stop ros_snapd_interfaces/srv/SnapdStop "service: 'ros2-nav2.slam'"
```

We can verify that our service is stopped with:

```
snap info ros2-nav2
```
