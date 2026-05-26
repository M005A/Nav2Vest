# NaviVest

NaviVest is a wearable real-time navigation assistance system designed for indoor and semi-structured environments. The system uses a chest-mounted stereo depth camera to detect traversable floor space, build a persistent local map, and generate guidance paths around obstacles in real time.

The current implementation is built on ROS 2 Jazzy using a Stereolabs ZED 2i stereo camera and a custom top-down path planner optimized for low-latency guidance and visualization.

---

## Features

- Real-time floor plane estimation using RANSAC
- Top-down occupancy grid generation from stereo depth
- Persistent rolling world memory
- Directional path planning with obstacle avoidance
- Dynamic unit-based replanning
- Camera trajectory visualization in RViz
- Path guidance output:
  - `FORWARD`
  - `LEFT`
  - `RIGHT`
  - `STOP!`
- Rotational heading-aware planning
- Persistent obstacle memory for large objects
- Real-time RViz visualization
- SVO playback support for offline testing

---

## System Overview

The planner operates in several stages:

1. Acquire point cloud data from the ZED 2i
2. Estimate the floor plane
3. Project the environment into a top-down occupancy grid
4. Store traversable and occupied regions in rolling memory
5. Generate a forward path within the current planning unit
6. Produce directional guidance relative to the user’s heading
7. Advance planning units as the user progresses

The planner keeps local planning stable by anchoring path generation to the current active unit rather than regenerating entirely from the live camera frame every update.

---

## Repository Structure

```text
src/
├── navivest_guidance/
│   ├── navivest_guidance/
│   │   └── zed_topdown_astar.py
│   └── package.xml
│
├── navivest_bringup/
│   ├── launch/
│   ├── rviz/
│   └── package.xml
│
└── ...
```

---

## Requirements

### Hardware

- NVIDIA GPU with CUDA support
- Stereolabs ZED 2i
- USB 3.0 connection
- Ubuntu 24.04 recommended

### Software

- ROS 2 Jazzy
- ZED SDK
- Python 3.12
- OpenCV
- NumPy

---

## Workspace Setup

Clone the repository:

```bash
git clone git@github.com:M005A/Nav2Vest.git
cd Nav2Vest
```

Build the workspace:

```bash
colcon build --symlink-install
source install/setup.bash
```

---

## Running NaviVest

### Live Camera

```bash
ros2 launch navivest_bringup navivest_full.launch.py
```

### SVO Playback

```bash
ros2 launch navivest_bringup navivest_full_svo.launch.py \
  svo_name:=hallway.svo2 \
  guidance_start_m:=0.10
```

---

## RViz Visualization

The RViz configuration includes:

- ZED point cloud
- Occupancy grid
- Generated path
- Camera trajectory trail
- TF frames
- RGB camera feed

If RViz does not automatically load the configuration:

```bash
rviz2 -d src/navivest_bringup/rviz/navivest_svo_guidance.rviz
```

---

## Guidance Logic

Directional guidance is determined using a short lookahead probe along the generated path.

The planner evaluates the path approximately `0.25 m` ahead of the user and determines whether the user should continue straight, turn left, or turn right relative to the current path trajectory.

This approach reduces instability caused by local path noise while maintaining responsive corrections during movement.

---

## Persistent Mapping

The mapping system maintains obstacle memory across camera movement and panning.

Large obstacle regions remain stored even after leaving the camera field of view, preventing the planner from immediately attempting to route through previously observed objects.

Unknown regions do not overwrite existing map memory.

---

## Camera Trajectory

The system publishes a persistent camera trajectory marker in RViz:

```text
/navivest/camera_trajectory
```

The trajectory trail remains visible for the duration of the session and provides a visual history of the user’s movement through the environment.

---

## Debugging

Useful topics:

```bash
ros2 topic hz /navivest/occupancy_grid
ros2 topic hz /navivest/path

ros2 topic echo /navivest/guidance --once
```

Validate Python syntax:

```bash
python3 -m py_compile \
  src/navivest_guidance/navivest_guidance/zed_topdown_astar.py
```

---

## Known Limitations

- Heavy glass reflections and highly reflective floors can reduce depth reliability
- Rapid camera pitch changes may temporarily destabilize floor estimation
- Very narrow spaces may require additional planner tuning
- Large dynamic crowds are not yet specifically handled

---

## Future Work

- Semantic obstacle classification
- SLAM-based long-term mapping
- Outdoor navigation support
- Multi-floor environment handling

---

## License

This project is currently under active development and does not yet include a formal open-source license.
