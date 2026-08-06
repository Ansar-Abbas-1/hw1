from launch import LaunchDescription

from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable

from launch.substitutions import PathJoinSubstitution, Command

from launch_ros.actions import Node

from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Tell Gazebo where to find robot meshes
    gazebo_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            PathJoinSubstitution([
                FindPackageShare('armando_description')
            ]),
            ':',
            ''
        ]
    )


    # Read URDF file and create robot_description parameter
    robot_description = Command([
        'xacro ',
        PathJoinSubstitution([
            FindPackageShare('armando_description'),
            'urdf',
            'arm.urdf'
        ])
    ])


    # Start Gazebo
    gazebo = IncludeLaunchDescription(
        PathJoinSubstitution([
            FindPackageShare('ros_gz_sim'),
            'launch',
            'gz_sim.launch.py'
        ]),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items()
    )


    # Publish robot description
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'robot_description': robot_description
            }
        ],
        output='screen'
    )


    # Spawn robot in Gazebo
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic',
            '/robot_description',
            '-name',
            'armando'
        ],
        output='screen'
    )


    return LaunchDescription([
        gazebo_resource_path,
        gazebo,
        robot_state_publisher,
        spawn_robot
    ])
