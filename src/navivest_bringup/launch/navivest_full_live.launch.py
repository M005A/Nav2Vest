import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    rviz = LaunchConfiguration('rviz')

    zed_wrapper_dir = get_package_share_directory('zed_wrapper')
    navivest_dir = get_package_share_directory('navivest_bringup')

    zed_launch = os.path.join(
        zed_wrapper_dir,
        'launch',
        'zed_camera.launch.py'
    )

    scan_launch = os.path.join(
        navivest_dir,
        'launch',
        'zed_to_scan.launch.py'
    )

    nav2_launch = os.path.join(
        navivest_dir,
        'launch',
        'nav2_planner_with_local_costmap.launch.py'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'rviz',
            default_value='true',
            description='Start RViz with the demo'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(zed_launch),
            launch_arguments={
                'camera_model': 'zed2i',
            }.items()
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(scan_launch)
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_launch)
        ),

        Node(
            package='navivest_guidance',
            executable='goal_to_plan',
            name='goal_to_plan',
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            condition=IfCondition(rviz)
        ),
    ])
