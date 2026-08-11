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
