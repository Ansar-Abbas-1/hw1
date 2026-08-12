# Homework 1

This repository contains the implementation of **Homework 1**.

## Repository and Branch Structure

Each question is developed on a separate Git branch. Since later questions extend and modify the files created in earlier questions, each branch represents the corresponding stage of the homework.

| Question | Branch |
|----------|--------|
| Q1 | `main` |
| Q2 | `q2_complete` |
| Q3 | `q3_complete` |
| Q4 | `q4_complete` |

To reproduce a specific question, checkout its corresponding branch **before building the workspace**.

For example, to reproduce Q1:

```bash
git switch main
```

The source code, launch files, robot description, configuration files, and instructions on each branch correspond to that question's implementation.

> **Important:** Since later questions extend and modify files from earlier questions, always switch to the required branch before building the workspace.

---

# Q1 — Robot Description and RViz Visualization

## Objective

Q1 modifies the **Armando robot description** and provides a complete **RViz2 visualization setup**.

The implementation includes:

- A dedicated RViz launch file.
- `robot_state_publisher`.
- `joint_state_publisher`.
- RViz2 with a saved configuration.
- Modified collision geometries using primitive box shapes.

---

## Q1(a) — RViz Launch

The launch file is located at:

```text
armando_description/launch/armando_display.launch.py
```

It loads the robot description, starts the required ROS 2 nodes, and opens RViz2.

The launch file starts:

- `robot_state_publisher`
- `joint_state_publisher`
- `rviz2`

---

## Q1(b) — RViz Configuration

The RViz configuration is stored in:

```text
armando_description/config/
```

The configuration automatically loads the **RobotModel** display and uses the appropriate fixed frame for visualizing the robot.

---

## Q1(c) — Collision Geometry

The collision meshes of the URDF were replaced with primitive `<box>` geometries.

The dimensions and origins of the boxes were adjusted to approximately match the bounding boxes of the corresponding visual meshes.

The collision geometry can be inspected in RViz2 using:

```text
RobotModel → Collision Enabled
```

---

# Build and Run

After checking out the Q1 branch:

```bash
cd ~/ros2_ws
git switch main
colcon build
source install/setup.bash
```

Launch the robot visualization:

```bash
ros2 launch armando_description armando_display.launch.py
```

RViz2 should open and display the **Armando** robot with the configured RobotModel and collision geometry.

This completes the required implementation for **Q1(a), Q1(b), and Q1(c)**.


# Q2 — Sensors, Hardware Interface, Controllers, and Gazebo Simulation

## Objective

Q2 extends the Armando robot simulation by integrating **Gazebo**, **ros2_control**, and joint controllers.

The implementation includes:

- Creation of the `armando_gazebo` ROS 2 package.
- A Gazebo simulation launch file.
- Conversion of the robot description to **Xacro**.
- A `ros2_control` hardware interface for the robot joints.
- Integration of the Gazebo ROS 2 Control plugin.
- Configuration of joint controllers using a YAML file.
- Spawning of the joint state broadcaster and position controller.
- Verification that the hardware interface and controllers are correctly loaded.

---

## Q2(a) — Gazebo Package and Robot Spawning

A new ROS 2 package named:

```text
armando_gazebo
```

was created using the ROS 2 CLI.

A launch directory was added containing:

```text
armando_gazebo/launch/armando_world.launch.py
```

The launch file:

- Starts Gazebo.
- Loads the Armando robot description.
- Uses `ros_gz_sim` to spawn the robot.
- Publishes the robot description to `/robot_description`.
- Configures the Gazebo resource path required by the simulation.

The robot can be launched using:

```bash
ros2 launch armando_gazebo armando_world.launch.py
```

This starts the Gazebo simulation and spawns the Armando robot.

---

## Q2(b) — ros2_control Hardware Interface

The robot description was converted to **Xacro** to allow modular configuration of the robot and its hardware interfaces.

The main robot description is:

```text
armando_description/urdf/arm.urdf.xacro
```

The Xacro namespace was added to the robot definition:

```xml
xmlns:xacro="http://www.ros.org/wiki/xacro"
```

A separate hardware interface file was created:

```text
armando_description/urdf/armando_hardware_interface.xacro
```

This file contains a Xacro macro defining the `ros2_control` hardware interface for the robot joints.

The joints use the position command interface required for the position controller.

The hardware interface is included in the main robot description using:

```xml
<xacro:include filename="$(find armando_description)/urdf/armando_hardware_interface.xacro"/>
```

The robot description is processed using **Xacro** when the Gazebo launch file is executed.

---

## Q2(c) — Gazebo ros2_control Plugin and Controllers

The Gazebo ROS 2 Control plugin was added to the robot description to connect the simulated robot joints with the `ros2_control` framework.

The controller configuration is loaded from a YAML file containing the required controller definitions.

The implemented controllers include:

- `joint_state_broadcaster`
- `position_controller`

The controllers are spawned from the Gazebo launch file using the `controller_manager` package.

The launch file uses `RegisterEventHandler` and `OnProcessExit` to ensure that the controllers are started after the robot has been spawned in Gazebo.

The controller startup sequence is therefore:

```text
Gazebo
   ↓
Robot spawned
   ↓
ros2_control hardware interface loaded
   ↓
joint_state_broadcaster
   ↓
position_controller
```

---

## Build and Run

Checkout the Q2 branch before building:

```bash
cd ~/ros2_ws
git switch q2_complete
```

Build the workspace:

```bash
colcon build
source install/setup.bash
```

Launch the Gazebo simulation:

```bash
ros2 launch armando_gazebo armando_world.launch.py
```

---

## Verify Controllers

The loaded controllers can be checked using:

```bash
ros2 control list_controllers
```

The expected controllers include:

```text
joint_state_broadcaster
position_controller
```

Both controllers should be reported as:

```text
active
```

The controller manager can also be inspected using:

```bash
ros2 node list
```

The Gazebo ROS 2 Control integration should be visible through the corresponding controller manager and Gazebo control nodes.

---

## Result

The Q2 implementation successfully integrates the Armando robot with **Gazebo** and **ros2_control**.

The simulated robot is spawned in Gazebo, its joints are connected through the configured hardware interface, and the required controllers are loaded and activated through the controller manager.

This completes the required implementation for **Q2(a), Q2(b), and Q2(c)**.

# Q3 — Camera Sensor Integration

## Objective

Q3 extends the Gazebo simulation by adding a **camera sensor** to the Armando robot and publishing its images as a ROS 2 image topic.

The implementation includes:

- A camera link attached to the robot base.
- A fixed camera joint.
- A dedicated camera Xacro file.
- Gazebo camera sensor specifications.
- The Gazebo Sensors System plugin.
- A ROS 2–Gazebo image bridge.
- Verification of the published camera image using `rqt_image_view`.

---

## Q3(a) — Camera Link and Fixed Joint

A dedicated camera link was added to the robot description in:

```text
armando_description/urdf/arm.urdf.xacro
```

The camera is attached to `base_link` using a fixed joint.

The camera link contains the required visual and collision geometry and is positioned appropriately on the robot base.

The resulting structure is conceptually:

```text
base_link
    |
    └── camera_link
```

The camera joint is fixed because the camera does not require an independent degree of freedom for this task.

---

## Q3(b) — Gazebo Camera Sensor

A dedicated Xacro file was created in:

```text
armando_gazebo/urdf/armando_camera.xacro
```

The file contains a Xacro macro defining the Gazebo camera sensor and its required sensor specifications.

The camera configuration includes the required Gazebo sensor parameters such as:

- Camera type.
- Image resolution.
- Image format.
- Update rate.
- Camera topic configuration.

The Gazebo Sensors System plugin was also included to enable sensor simulation.

The camera Xacro file is imported into the main robot description using:

```xml
<xacro:include ... />
```

This keeps the camera sensor configuration separate from the main robot description and makes the robot model easier to maintain.

---

## Q3(c) — Gazebo Simulation and Image Topic

The Gazebo simulation is launched using the Gazebo launch file:

```text
armando_gazebo/launch/armando_world.launch.py
```

The launch configuration includes the required ROS 2–Gazebo bridge for the camera image topic.

The bridge converts the Gazebo camera image message into a ROS 2:

```text
sensor_msgs/msg/Image
```

topic.

The published image topic can be checked using:

```bash
ros2 topic list
```

The camera image topic should be visible in the list of available ROS 2 topics.

The topic information can be inspected using:

```bash
ros2 topic info /camera/image_raw
```

The expected message type is:

```text
sensor_msgs/msg/Image
```

---

## Build and Run

Checkout the Q3 branch before building:

```bash
cd ~/ros2_ws
git switch q3_complete
```

Build the workspace:

```bash
colcon build
source install/setup.bash
```

Launch the Gazebo simulation:

```bash
ros2 launch armando_gazebo armando_world.launch.py
```

---

## Verify the Camera Image

First, check that the camera image topic is available:

```bash
ros2 topic list
```

Then inspect the topic:

```bash
ros2 topic info /camera/image_raw
```

The topic should report:

```text
Type: sensor_msgs/msg/Image
```

The image can then be visualized using:

```bash
rqt_image_view
```

In `rqt_image_view`, select:

```text
/camera/image_raw
```

A live camera image from the simulated Armando robot should be displayed.

---

## Result

The Q3 implementation successfully integrates a simulated camera into the Armando robot.

The camera is attached to the robot through a fixed joint, simulated in Gazebo using the Gazebo Sensors System, and connected to ROS 2 through the Gazebo–ROS 2 bridge.

The resulting camera image is available as a ROS 2 image topic and can be visualized using `rqt_image_view`.

This completes the required implementation for **Q3(a), Q3(b), and Q3(c)**.

# Q4 — ROS Joint State and Joint Command Controller

## Objective

Q4 introduces a dedicated ROS 2 C++ controller node for the Armando robot.

The node:

- Subscribes to the robot joint states.
- Prints the current joint positions.
- Publishes sequential joint position commands.
- Publishes equivalent joint trajectory commands.
- Allows the user to select between position and trajectory control.
- Loads only the controller corresponding to the selected control mode.

---

## Q4(a) — ROS 2 C++ Controller Package

A new ROS 2 package named:

```text
armando_controller
```

was created.

The package contains the C++ node:

```text
arm_controller_node
```

The main source file is located in:

```text
armando_controller/src/arm_controller_node.cpp
```

The package was configured with the required ROS 2 dependencies, including:

- `rclcpp`
- `sensor_msgs`
- `std_msgs`
- `trajectory_msgs`

The `CMakeLists.txt` and `package.xml` files were updated to build and link the controller node correctly.

---

## Q4(b) — Joint State Subscriber

The controller node subscribes to:

```text
/joint_states
```

using:

```text
sensor_msgs/msg/JointState
```

The callback reads the joint names and their current positions and prints them to the terminal.

For example, the node reports joint positions in radians:

```text
Joint: j0, Position: ...
Joint: j1, Position: ...
Joint: j2, Position: ...
Joint: j3, Position: ...
```

This provides feedback about the current state of the simulated robot.

---

## Q4(c) — Sequential Position Commands

The node publishes position commands using:

```text
/position_controller/commands
```

with message type:

```text
std_msgs/msg/Float64MultiArray
```

Four different joint configurations are sent sequentially.

The implemented configurations are:

```text
[0.0, 0.0, 0.0, 0.0]
[0.4, 0.0, 0.0, 0.0]
[0.4, 0.4, 0.0, 0.0]
[0.0, 0.0, 0.4, 0.0]
```

The commands are sent at three-second intervals.

The position controller is loaded when the node is launched in position mode.

---

## Q4(d) — Joint Trajectory Control and Mode Selection

A joint trajectory publisher was added to send the same four configurations through the trajectory controller.

The trajectory topic is:

```text
/trajectory_controller/joint_trajectory
```

with message type:

```text
trajectory_msgs/msg/JointTrajectory
```

The trajectory contains the four robot joint names:

```text
j0
j1
j2
j3
```

Each requested configuration is sent as a trajectory point with:

```text
time_from_start = 1 second
```

Therefore, each commanded configuration is reached approximately one second after the trajectory is started.

### Control Mode Selection

The user can select the controller mode through the ROS 2 launch argument:

```text
control_mode
```

Two modes are supported:

```text
position
trajectory
```

The default mode is:

```text
position
```

The launch file passes the selected mode to `arm_controller_node` as a ROS parameter.

In addition, the launch file starts only the corresponding controller:

- `position` → `position_controller`
- `trajectory` → `trajectory_controller`

The `joint_state_broadcaster` is loaded in both modes.

This prevents both command controllers from being active simultaneously.

---

## Build

Checkout the Q4 branch:

```bash
cd ~/ros2_ws
git switch q4_complete
```

Build the workspace:

```bash
colcon build
source install/setup.bash
```

---

## Run — Position Mode

Position mode is the default:

```bash
ros2 launch armando_gazebo armando_world.launch.py
```

Alternatively, it can be selected explicitly:

```bash
ros2 launch armando_gazebo armando_world.launch.py control_mode:=position
```

The active controllers can be checked using:

```bash
ros2 control list_controllers
```

The expected active controllers include:

```text
joint_state_broadcaster
position_controller
```

The position command topic can be verified with:

```bash
ros2 topic info /position_controller/commands
```

Expected message type:

```text
std_msgs/msg/Float64MultiArray
```

---

## Run — Trajectory Mode

Trajectory mode can be selected using:

```bash
ros2 launch armando_gazebo armando_world.launch.py control_mode:=trajectory
```

Check the active controllers:

```bash
ros2 control list_controllers
```

The expected active controllers include:

```text
joint_state_broadcaster
trajectory_controller
```

The trajectory topic can be verified with:

```bash
ros2 topic info /trajectory_controller/joint_trajectory
```

Expected message type:

```text
trajectory_msgs/msg/JointTrajectory
```

The published trajectory can also be inspected using:

```bash
ros2 topic echo /trajectory_controller/joint_trajectory
```

---

## Verification

The controller node can be confirmed using:

```bash
ros2 node list
```

The node should appear as:

```text
/arm_controller_node
```

The joint states can be inspected using:

```bash
ros2 topic echo /joint_states
```

During trajectory-mode testing, the commanded joint configuration was verified through the joint-state feedback. For example, after sending:

```text
[0.0, 0.0, 0.4, 0.0]
```

the measured joint state showed approximately:

```text
j0 = 0.0 rad
j1 = 0.0 rad
j2 = 0.4 rad
j3 = 0.0 rad
```

confirming that the trajectory controller successfully moved `j2` to the requested position.

---

## Result

Q4 provides a complete ROS 2 C++ controller for the Armando robot.

The implementation supports both direct joint-position control and joint-trajectory control, with the control method selected through the `control_mode` launch argument.

This completes the required implementation for **Q4(a), Q4(b), Q4(c), and Q4(d)**.
