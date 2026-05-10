import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_dir = get_package_share_directory('navivest_bringup')
    params_file = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')

    lifecycle_nodes = [
        'planner_server',
        'controller_server',
    ]

    return LaunchDescription([
        # Planner server gives:
        # /global_costmap/costmap
        # /compute_path_to_pose
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[params_file],
        ),

        # Controller server gives:
        # /local_costmap/costmap
        # We are NOT using it for robot control right now.
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[params_file],
        ),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_planning',
            output='screen',
            parameters=[{
                'use_sim_time': False,
                'autostart': True,
                'node_names': lifecycle_nodes,
            }],
        ),
    ])
