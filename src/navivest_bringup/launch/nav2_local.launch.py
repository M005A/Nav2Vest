import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_dir = get_package_share_directory('navivest_bringup')
    params_file = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')

    return LaunchDescription([
        Node(
            package='nav2_controller',
            executable='controller_server',
            output='screen',
            parameters=[params_file],
        ),
        Node(
            package='nav2_planner',
            executable='planner_server',
            output='screen',
            parameters=[params_file],
        ),
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            output='screen',
            parameters=[params_file],
        ),
        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            output='screen',
            parameters=[params_file],
        ),
        Node(
            package='nav2_waypoint_follower',
            executable='waypoint_follower',
            output='screen',
            parameters=[params_file],
        ),
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[{
                'use_sim_time': False,
                'autostart': True,
                'node_names': [
                    'controller_server',
                    'planner_server',
                    'bt_navigator',
                    'behavior_server',
                    'waypoint_follower',
                ]
            }]
        ),
    ])
