import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def launch_setup(context, *args, **kwargs):
    svo_path = LaunchConfiguration('svo_path').perform(context)
    svo_file = LaunchConfiguration('svo_file').perform(context)
    recording = LaunchConfiguration('recording').perform(context)
    svo = LaunchConfiguration('svo').perform(context)
    svo_name = LaunchConfiguration('svo_name').perform(context)
    camera_model = LaunchConfiguration('camera_model')
    rviz = LaunchConfiguration('rviz')
    guidance_start_m = float(LaunchConfiguration('guidance_start_m').perform(context))

    if not svo_path and svo_file:
        svo_path = svo_file
    if not svo_path and recording:
        svo_path = recording
    if not svo_path and svo:
        svo_path = svo
    if not svo_path and svo_name:
        svo_path = os.path.join('/home/macho/navivest_datasets/recordings', svo_name)

    if svo_path and not os.path.isabs(os.path.expanduser(svo_path)):
        svo_path = os.path.join('/home/macho/navivest_datasets/recordings', svo_path)

    if not svo_path or svo_path == 'live':
        raise RuntimeError(
            'navivest_full_svo requires an SVO file. Use '
            'svo_name:=02_chair_center.svo2 or svo_path:=/absolute/path/file.svo2'
        )

    svo_path = os.path.abspath(os.path.expanduser(svo_path))
    if not os.path.isfile(svo_path):
        raise RuntimeError(f'SVO file does not exist: {svo_path}')

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
    rviz_config = os.path.join(
        navivest_dir,
        'rviz',
        'navivest_svo_guidance.rviz'
    )

    return [
        LogInfo(msg=f'NaviVest SVO playback: {svo_path}'),
        LogInfo(msg=f'NaviVest guidance_start_m: {guidance_start_m:.2f}'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(zed_launch),
            launch_arguments={
                'camera_model': camera_model,
                'svo_path': svo_path,
                'publish_svo_clock': 'true',
                'ros_params_override_path': zed_config,
            }.items()
        ),

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
                'min_range_m': 0.55,
                'guidance_start_m': guidance_start_m,
                'min_obstacle_height_m': 0.07,
                'max_obstacle_height_m': 2.20,
                'min_obstacle_points_per_cell': 1,
                'floor_free_band_m': 0.12,
                'free_space_dilation_m': 0.35,
                'camera_floor_band_m': 0.12,
                'use_camera_axis_fallback': False,
                'inflation_radius_m': 0.06,
                'planning_inflation_radius_m': 0.06,
                'clear_width_m': 0.26,
                'obstacle_hold_frames': 8,
                'display_obstacle_hold_frames': 1,
                'planning_obstacle_hold_frames': 6,
                'free_space_hold_frames': 18,
                'max_lateral_step_cells': 2,
                'path_switch_min_gain_m': 0.55,
                'reroute_min_forward_gain_m': 0.75,
                'prepend_camera_anchor': True,
                'max_points': 50000,
                'max_ransac_points': 14000,
                'process_hz': 30.0,
                'floor_ransac_iters': 70,
                'floor_dist_thresh_m': 0.045,
                'min_floor_inliers': 700,
                'floor_normal_min_abs_y': 0.45,
                'publish_debug': False,
                'debug_scale': 2,
                'path_stride_cells': 4,
                'stats_period_s': 2.0,
            }]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            output='screen',
            condition=IfCondition(rviz)
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'svo_path',
            default_value='',
            description='Path to SVO/SVO2 file'
        ),
        DeclareLaunchArgument(
            'svo_file',
            default_value='',
            description='Alias for svo_path; accepts absolute path or dataset filename'
        ),
        DeclareLaunchArgument(
            'recording',
            default_value='',
            description='Alias for svo_path; accepts absolute path or dataset filename'
        ),
        DeclareLaunchArgument(
            'svo',
            default_value='',
            description='Alias for svo_path; accepts absolute path or dataset filename'
        ),
        DeclareLaunchArgument(
            'svo_name',
            default_value='',
            description='Filename inside /home/macho/navivest_datasets/recordings'
        ),
        DeclareLaunchArgument(
            'guidance_start_m',
            default_value='0.10',
            description='Straight-ahead distance from the camera before the guidance path may turn'
        ),
        DeclareLaunchArgument(
            'camera_model',
            default_value='zed2i',
            description='ZED camera model for the recording; use zed for older .svo recordings'
        ),
        DeclareLaunchArgument(
            'rviz',
            default_value='true',
            description='Start RViz with the demo'
        ),

        OpaqueFunction(function=launch_setup),
    ])
