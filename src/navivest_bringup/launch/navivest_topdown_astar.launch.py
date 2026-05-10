import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
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

    zed_config = os.path.join(
        navivest_dir,
        'config',
        'zed2i.yaml'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(zed_launch),
            launch_arguments={
                'camera_model': 'zed2i',
                'ros_params_override_path': zed_config,
            }.items()
        ),

        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package='navivest_guidance',
                    executable='zed_topdown_astar',
                    name='zed_topdown_astar',
                    output='screen',
                    parameters=[{
                        'cloud_topic': '/zed/zed_node/point_cloud/cloud_registered',
                        'grid_frame': 'zed_left_camera_frame',
                        'grid_width_m': 5.0,
                        'grid_forward_m': 5.0,
                        'resolution_m': 0.05,
                        'min_obstacle_height_m': 0.04,
                        'max_obstacle_height_m': 2.0,
                        'camera_floor_band_m': 0.12,
                        'inflation_radius_m': 0.30,
                        'clear_width_m': 0.60,
                        'max_points': 40000,
                        'max_ransac_points': 12000,
                        'process_hz': 30.0,
                        'floor_ransac_iters': 45,
                        'floor_dist_thresh_m': 0.05,
                        'min_floor_inliers': 500,
                        'floor_normal_min_abs_y': 0.55,
                        'publish_debug': True,
                        'debug_scale': 2,
                        'path_stride_cells': 2,
                }]
                ),

                Node(
                    package='rviz2',
                    executable='rviz2',
                    name='rviz2',
                    output='screen'
                ),
            ]
        ),
    ])
