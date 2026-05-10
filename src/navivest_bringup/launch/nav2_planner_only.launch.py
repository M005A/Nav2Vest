import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_dir = get_package_share_directory('navivest_bringup')
    params_file = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')

    lifecycle_nodes = [
        'planner_server',
    ]

    return LaunchDescription([
        Node(
            package='nav2_planner',
            executable='planner_server',
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
