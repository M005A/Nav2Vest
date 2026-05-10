import os


from launch import LaunchDescription
from launch.actions import TimerAction
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    zed_wrapper_dir = get_package_share_directory('zed_wrapper')
    navivest_dir = get_package_share_directory('navivest_bringup')

    zed_launch = os.path.join(
        zed_wrapper_dir,
        'launch',
        'zed_camera.launch.py'
    )

    planner_launch = os.path.join(
        navivest_dir,
        'launch',
        'nav2_planner_only.launch.py'
    )
    
    controller_launch = os.path.join(
    navivest_dir,
    'launch',
    'nav2_controller_only.launch.py'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(zed_launch),
            launch_arguments={
                'camera_model': 'zed2i',
                'config_path': os.path.join(navivest_dir, 'config', 'zed2i.yaml'),

            }.items()
        ),

    TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(planner_launch)
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(controller_launch)
            ),
        ]
    ),        

        Node(
            package='navivest_guidance',
            executable='goal_to_plan',
            name='goal_to_plan',
            output='screen'
        ),

        Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='zed_to_base',
            arguments=[
                '0', '0', '-1.2',           # x y z: camera is 1.2m above floor
                '0', '0', '0', # rotation placeholder
                'zed_camera_link',
                'base_link'
            ],
        ),   

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        ),
    ])
