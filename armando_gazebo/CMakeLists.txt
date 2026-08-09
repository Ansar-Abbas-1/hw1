cmake_minimum_required(VERSION 3.8)
project(armando_gazebo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find the ROS 2 CMake build system
find_package(ament_cmake REQUIRED)

# Install the launch directory so ROS 2 can find launch files after building
install(
  DIRECTORY 
  launch
  urdf
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)

  # Skip copyright check (default template)
  set(ament_cmake_copyright_FOUND TRUE)

  # Skip cpplint check (default template)
  set(ament_cmake_cpplint_FOUND TRUE)

  ament_lint_auto_find_test_dependencies()
endif()

# Register this package with the ROS 2 build system
ament_package()
