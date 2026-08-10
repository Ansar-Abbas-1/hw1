cmake_minimum_required(VERSION 3.8)
project(armando_controller)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)

# Create the arm controller executable
add_executable(arm_controller_node
  src/arm_controller_node.cpp
)

# Link ROS 2 dependencies to the executable
ament_target_dependencies(arm_controller_node
  rclcpp
  sensor_msgs
  std_msgs
)

# Install the executable
install(
  TARGETS arm_controller_node
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)

  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)

  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
