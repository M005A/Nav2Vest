import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


# Live ZED camera constants. The actual SDK camera open is performed by
# zed_wrapper's zed_camera.launch.py, which uses sl.Camera() internally.
LIVE_CAMERA_INDEX = "-1"
SERIAL_NUMBER = "0"
CAMERA_RESOLUTION = "HD720"
CAMERA_FPS = 30
DEPTH_MODE = "NEURAL_LIGHT"


def launch_setup(context, *args, **kwargs):
    camera_model = LaunchConfiguration('camera_model')
    camera_id = LaunchConfiguration('camera_id')
    serial_number = LaunchConfiguration('serial_number')
    rviz = LaunchConfiguration('rviz')
    audio = LaunchConfiguration('audio')
    audio_voice_cmd = LaunchConfiguration('audio_voice_cmd')
    audio_min_repeat_s = float(LaunchConfiguration('audio_min_repeat_s').perform(context))
    guidance_start_m = float(LaunchConfiguration('guidance_start_m').perform(context))

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
        LogInfo(msg='NaviVest live ZED camera guidance'),
        LogInfo(msg=f'NaviVest live camera resolution: {CAMERA_RESOLUTION}'),
        LogInfo(msg=f'NaviVest live camera FPS: {CAMERA_FPS}'),
        LogInfo(msg=f'NaviVest live depth mode: {DEPTH_MODE}'),
        LogInfo(msg=f'NaviVest guidance_start_m: {guidance_start_m:.2f}'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(zed_launch),
            launch_arguments={
                'camera_model': camera_model,
                'svo_path': 'live',
                'camera_id': camera_id,
                'serial_number': serial_number,
                'publish_svo_clock': 'false',
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
                'odom_topic': '/zed/zed_node/odom',
                'grid_frame': 'zed_left_camera_frame',
                'odom_frame': 'odom',
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
                'enable_pose_grid_memory': True,
                'memory_forward_grid_count': 3,
                'memory_lateral_grid_count': 3,
                'replan_only_on_grid_exit': False,
                'replan_on_path_obstruction': True,
                'replan_heading_delta_rad': 0.45,
                'unit_goal_reached_m': 0.35,
                'guidance_topic': '/navivest/guidance',
                'audio_cue_topic': '/navivest/audio_cue',
                'stop_path_distance_m': 0.35,
                'audio_path_check_step_m': 0.10,
                'audio_upcoming_turn_min_distance_m': 0.25,
                'audio_upcoming_turn_max_distance_m': 0.75,
                'audio_direction_change_lateral_threshold_m': 0.12,
                'guidance_first_turn_lookahead_m': 1.10,
                'guidance_turn_lateral_threshold_m': 0.15,
                'guidance_ignore_near_m': 0.08,
                'guidance_debounce_frames': 4,
                'guidance_stop_debounce_frames': 2,
                'guidance_log_period_s': 0.5,
                'invert_guidance_lr': False,
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
            package='navivest_guidance',
            executable='guidance_audio',
            name='guidance_audio',
            output='screen',
            parameters=[{
                'topic': '/navivest/audio_cue',
                'voice_cmd': audio_voice_cmd,
                'min_repeat_s': audio_min_repeat_s,
            }],
            condition=IfCondition(audio),
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
            'guidance_start_m',
            default_value='0.10',
            description='Straight-ahead distance from the camera before the guidance path may turn'
        ),
        DeclareLaunchArgument(
            'camera_model',
            default_value='zed2i',
            description='Live ZED camera model'
        ),
        DeclareLaunchArgument(
            'camera_id',
            default_value=LIVE_CAMERA_INDEX,
            description='Live camera ID; -1 lets the ZED SDK choose the connected camera'
        ),
        DeclareLaunchArgument(
            'serial_number',
            default_value=SERIAL_NUMBER,
            description='Live camera serial number; 0 lets the ZED SDK choose the connected camera'
        ),
        DeclareLaunchArgument(
            'audio',
            default_value='true',
            description='Speak NaviVest audio cues from /navivest/audio_cue'
        ),
        DeclareLaunchArgument(
            'audio_voice_cmd',
            default_value='spd-say',
            description='Speech command used by guidance_audio; use espeak if speech-dispatcher is unavailable'
        ),
        DeclareLaunchArgument(
            'audio_min_repeat_s',
            default_value='1.5',
            description='Minimum seconds before repeating the same spoken cue'
        ),
        DeclareLaunchArgument(
            'rviz',
            default_value='true',
            description='Start RViz with the demo'
        ),

        OpaqueFunction(function=launch_setup),
    ])
