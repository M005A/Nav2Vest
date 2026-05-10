from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            output='screen',
            remappings=[
                ('cloud_in', '/zed/zed_node/point_cloud/cloud_registered'),
                ('scan', '/scan'),
            ],
            parameters=[{
                'target_frame': 'zed_camera_link',
                'transform_tolerance': 0.2,

                # More aggressive floor rejection.
                # If floor still appears, raise min_height.
                # If chair disappears, lower min_height.
                'min_height': -0.10,
                'max_height': 0.85,

                # Limit to forward-facing region.
                'angle_min': -0.80,
                'angle_max': 0.80,
                'angle_increment': 0.035,

                'scan_time': 0.10,
                'range_min': 0.55,
                'range_max': 3.5,

                'use_inf': True,
                'inf_epsilon': 1.0,
            }]
        )
    ])
