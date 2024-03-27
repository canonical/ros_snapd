cmake_minimum_required(VERSION 3.16)
project(ros_snapd)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  rospy
  std_msgs
)

catkin_python_setup()

add_service_files(
  FILES
  SnapdList.srv
  SnapdStatus.srv
  SnapdStart.srv
  SnapdRestart.srv
  SnapdStop.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package()

catkin_install_python(PROGRAMS scripts/ros_snapd
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
