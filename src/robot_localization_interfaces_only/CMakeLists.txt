cmake_minimum_required(VERSION 3.8)
project(robot_localization)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(geographic_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/FromLL.srv"
  "srv/FromLLArray.srv"
  "srv/GetState.srv"
  "srv/SetDatum.srv"
  "srv/SetPose.srv"
  "srv/SetUTMZone.srv"
  "srv/ToLL.srv"
  "srv/ToLLArray.srv"
  "srv/ToggleFilterProcessing.srv"
  DEPENDENCIES builtin_interfaces geographic_msgs geometry_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
