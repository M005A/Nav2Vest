from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan',
            output='screen',
            remappings=[
                ('depth', '/zed/zed_node/depth/depth_registered'),
                ('depth_camera_info', '/zed/zed_node/depth/depth_registered/camera_info'),
                ('scan', '/scan'),
            ],
            parameters=[{
                'scan_height': 10,
                'scan_time': 0.2,
                'range_min': 0.55,
                'range_max': 3.5,
                'output_frame': 'zed_camera_link',
            }]
        )
    ])
