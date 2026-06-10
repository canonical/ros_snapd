cmake_minimum_required(VERSION 3.16)
project(ros_snapd)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_python_setup()

catkin_package()

catkin_install_python(PROGRAMS scripts/ros_snapd
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
