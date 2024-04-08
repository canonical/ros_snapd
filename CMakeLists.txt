cmake_minimum_required(VERSION 3.16)
project(ros2_snapd)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/SnapdList.srv"
  "srv/SnapdStart.srv"
  "srv/SnapdRestart.srv"
  "srv/SnapdStop.srv"
)

install(PROGRAMS
  scripts/ros2_snapd.py
  RENAME ros2_snapd
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()

  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_snapd_interface tests/test_snapd_interface.py
    APPEND_ENV PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}
    TIMEOUT 60
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  )
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package()
