# Contributing

Any contribution that you make to this repository will
be under the GNU General Public License, as dictated by that
[license](https://opensource.org/licenses/GPL-3.0).

## Setup a development environment

The simpler manner to setup a ROS ready development environment is using Multipass:

```bash
multipass launch ros-noetic -n ros-noetic-vm
```

You can then shell to the vm with:

```bash
multipass shell ros2-noetic-vm
```

And create the project,

```bash
mkdir -p workspace/src
cd workspace/src
git clone https://github.com/ubuntu-robotics/ros_snapd.git -b noetic
```

Make sure that all dependencies are available,

```bash
rosdep install --default-yes --ignore-packages-from-source --rosdistro=noetic --from-paths .
```

Install also the `snap-http` Python3 module,

```bash
apt install python3-pip
python3 -m pip install -r requirements.txt
```

At this point you can build the project,

```bash
cd ~/workspace
catkin build
```

To run the tests enter:

```bash
catkin test
```
