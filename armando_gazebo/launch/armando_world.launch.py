
from launch import LaunchDescription

from launch.actions import (
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    RegisterEventHandler
)

from launch.event_handlers import OnProcessExit

from launch.substitutions import PathJoinSubstitution, Command

from launch_ros.actions import Node

from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


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
            'arm.urdf.xacro'
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
                'robot_description': ParameterValue(
                    robot_description,
                    value_type=str
                )
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
    
    
    
    joint_state_broadcaster = Node(
    package='controller_manager',
    executable='spawner',
    arguments=[
        'joint_state_broadcaster',
        '--controller-manager',
        '/controller_manager'
    ],
    output='screen'
    )
    
    
    position_controller = Node(
    package='controller_manager',
    executable='spawner',
    arguments=[
        'position_controller',
        '--controller-manager',
        '/controller_manager'
    ],
    output='screen'
    )


    delay_joint_state_broadcaster = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot,
            on_exit=[
                joint_state_broadcaster
            ]
        )
    )


    delay_position_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot,
            on_exit=[
                position_controller
            ]
        )
    )



    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image'
        ],
        output='screen'
    )



    return LaunchDescription([
        gazebo_resource_path,

        gazebo,

        robot_state_publisher,

        spawn_robot,

        delay_joint_state_broadcaster,

        delay_position_controller,
        ros_gz_bridge
    ])
