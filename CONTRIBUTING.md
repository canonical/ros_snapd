# Contributing

Any contribution that you make to this repository will
be under the GNU General Public License, as dictated by that
[license](https://opensource.org/licenses/GPL-3.0).

## Setup a development environment

The simpler manner to setup a ROS 2 ready development environment is using Multipass:

```bash
multipass launch ros2-humble -n ros2-humble-vm
```

You can then shell to the vm with:

```bash
multipass shell ros2-humble-vm
```

And create the project,

```bash
mkdir -p workspace/src
cd workspace/src
git clone https://github.com/ubuntu-robotics/ros_snapd.git -b humble
```

Make sure that all dependencies are available,

```bash
rosdep install --default-yes --ignore-packages-from-source --rosdistro=humble --from-paths .
```

Install also the `snap-http` Python3 module,

```bash
apt install python3-pip
python3 -m pip install snap-http
```

At this point you can build the project,

```bash
cd ~/workspace
colcon build --symlink-install
```

To run the tests enter:

```bash
colcon test
colcon test-results --all --verbose
```
