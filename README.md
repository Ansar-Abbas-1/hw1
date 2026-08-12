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
