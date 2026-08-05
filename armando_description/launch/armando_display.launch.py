from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    package_path = get_package_share_directory("armando_description")

    urdf_path = os.path.join(
        package_path,
        "urdf",
        "arm.urdf"
    )

    with open(urdf_path, "r") as file:
        robot_description = file.read()

    return LaunchDescription([

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[
                {"robot_description": robot_description}
            ]
        ),

        Node(
            package="joint_state_publisher",
            executable="joint_state_publisher",
            output="screen"
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            output="screen"
        )

    ])
