from launch import LaunchDescription

from launch.actions import (
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    RegisterEventHandler,
    DeclareLaunchArgument
)

from launch.conditions import IfCondition

from launch.event_handlers import OnProcessExit

from launch.substitutions import (
    PathJoinSubstitution,
    Command,
    LaunchConfiguration,
    PythonExpression
)

from launch_ros.actions import Node

from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # ---------------------------------------------------------
    # Controller mode argument
    # ---------------------------------------------------------

    control_mode = LaunchConfiguration('control_mode')

    control_mode_arg = DeclareLaunchArgument(
        'control_mode',
        default_value='position',
        description='Controller mode: position or trajectory'
    )


    # ---------------------------------------------------------
    # Gazebo resource path
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # Read URDF
    # ---------------------------------------------------------

    robot_description = Command([
        'xacro ',
        PathJoinSubstitution([
            FindPackageShare('armando_description'),
            'urdf',
            'arm.urdf.xacro'
        ])
    ])


    # ---------------------------------------------------------
    # Start Gazebo
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # Robot State Publisher
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # Spawn robot
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # Joint State Broadcaster
    # Always required
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # Position Controller
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # Trajectory Controller
    # ---------------------------------------------------------

    trajectory_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'trajectory_controller',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )
    
    # ---------------------------------------------------------
    # Arm Controller Node
    # Receives the selected control mode
    # ---------------------------------------------------------
    
    arm_controller_node = Node(
	package='armando_controller',
	executable='arm_controller_node',
	parameters=[
	    {
		'control_mode': control_mode
	    }
	],
	output='screen'
    )


    # ---------------------------------------------------------
    # Start Joint State Broadcaster after robot is spawned
    # ---------------------------------------------------------

    delay_joint_state_broadcaster = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot,
            on_exit=[
                joint_state_broadcaster
            ]
        )
    )


    # ---------------------------------------------------------
    # Start Position Controller ONLY in position mode
    # ---------------------------------------------------------

    delay_position_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot,
            on_exit=[
                position_controller
            ]
        ),
        condition=IfCondition(
            PythonExpression([
                "'",
                control_mode,
                "' == 'position'"
            ])
        )
    )


    # ---------------------------------------------------------
    # Start Trajectory Controller ONLY in trajectory mode
    # ---------------------------------------------------------

    delay_trajectory_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot,
            on_exit=[
                trajectory_controller
            ]
        ),
        condition=IfCondition(
            PythonExpression([
                "'",
                control_mode,
                "' == 'trajectory'"
            ])
        )
    )


    # ---------------------------------------------------------
    # Camera bridge
    # ---------------------------------------------------------

    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image'
        ],
        output='screen'
    )


    # ---------------------------------------------------------
    # Launch everything
    # ---------------------------------------------------------

    return LaunchDescription([
        control_mode_arg,

        gazebo_resource_path,

        gazebo,

        robot_state_publisher,

        spawn_robot,

        delay_joint_state_broadcaster,

        delay_position_controller,

        delay_trajectory_controller,
        arm_controller_node,

        ros_gz_bridge,
    ])
