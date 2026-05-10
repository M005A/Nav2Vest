import math
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from nav2_msgs.action import ComputePathToPose


class GoalToPlan(Node):
    def __init__(self):
        super().__init__('goal_to_plan')

        self.global_frame = 'zed_camera_link'
        self.planner_id = 'GridBased'

        self.last_goal = None
        self.last_request_time = 0.0
        self.replan_period = 0.33

        self.request_in_progress = False
        self.pending_candidates = []
        self.current_candidate_index = 0

        self.client = ActionClient(
            self,
            ComputePathToPose,
            '/compute_path_to_pose'
        )

        self.goal_sub = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )

        self.plan_pub = self.create_publisher(
            Path,
            '/plan',
            10
        )

        self.timer = self.create_timer(self.replan_period, self.timer_callback)

        self.get_logger().info('goal_to_plan started')
        self.get_logger().info('Click 2D Goal Pose in RViz')

    def goal_callback(self, msg: PoseStamped):
        self.last_goal = msg
        self.get_logger().info(
            f'New goal: x={msg.pose.position.x:.2f}, y={msg.pose.position.y:.2f}'
        )
        self.try_request_plan()

    def timer_callback(self):
        if self.last_goal is None:
            return

        now = time.time()
        if now - self.last_request_time < self.replan_period:
            return

        self.try_request_plan()

    def try_request_plan(self):
        if self.request_in_progress:
            return

        if self.last_goal is None:
            return

        self.pending_candidates = self.make_goal_candidates(self.last_goal)
        self.current_candidate_index = 0
        self.request_next_candidate()

    def make_goal_candidates(self, goal_msg):
        x = goal_msg.pose.position.x
        y = goal_msg.pose.position.y

        # Candidate offsets in the camera/body frame.
        # x = forward, y = left/right.
        lateral_offsets = [0.0, 0.25, -0.25, 0.45, -0.45, 0.70, -0.70]
        forward_scales = [1.0, 0.85, 0.70]

        candidates = []

        for scale in forward_scales:
            for offset in lateral_offsets:
                candidate = PoseStamped()
                candidate.header.frame_id = self.global_frame
                candidate.header.stamp = self.get_clock().now().to_msg()

                candidate.pose.position.x = x * scale
                candidate.pose.position.y = y + offset
                candidate.pose.position.z = 0.0
                candidate.pose.orientation = goal_msg.pose.orientation

                candidates.append(candidate)

        return candidates

    def request_next_candidate(self):
        if self.current_candidate_index >= len(self.pending_candidates):
            self.publish_empty_plan()
            self.get_logger().warn('No candidate goal produced a valid path. Published empty /plan.')
            self.request_in_progress = False
            return

        if not self.client.wait_for_server(timeout_sec=0.1):
            self.get_logger().warn('Planner action /compute_path_to_pose not available')
            self.publish_empty_plan()
            self.request_in_progress = False
            return

        goal = self.pending_candidates[self.current_candidate_index]

        start = PoseStamped()
        start.header.frame_id = self.global_frame
        start.header.stamp = self.get_clock().now().to_msg()
        start.pose.position.x = 0.0
        start.pose.position.y = 0.0
        start.pose.position.z = 0.0
        start.pose.orientation.w = 1.0

        request = ComputePathToPose.Goal()
        request.start = start
        request.goal = goal
        request.planner_id = self.planner_id
        request.use_start = True

        self.last_request_time = time.time()
        self.request_in_progress = True

        future = self.client.send_goal_async(request)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        try:
            goal_handle = future.result()
        except Exception as exc:
            self.get_logger().warn(f'Planner goal request failed: {exc}')
            self.current_candidate_index += 1
            self.request_next_candidate()
            return

        if not goal_handle.accepted:
            self.get_logger().warn('Planner rejected candidate goal')
            self.current_candidate_index += 1
            self.request_next_candidate()
            return

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        try:
            result = future.result().result
        except Exception as exc:
            self.get_logger().warn(f'Planner result failed: {exc}')
            self.current_candidate_index += 1
            self.request_next_candidate()
            return

        if not result.path.poses:
            self.current_candidate_index += 1
            self.request_next_candidate()
            return

        self.plan_pub.publish(result.path)
        self.request_in_progress = False

        goal = self.pending_candidates[self.current_candidate_index].pose.position
        self.get_logger().info(
            f'Published /plan with {len(result.path.poses)} poses '
            f'to candidate x={goal.x:.2f}, y={goal.y:.2f}'
        )

    def publish_empty_plan(self):
        empty = Path()
        empty.header.frame_id = self.global_frame
        empty.header.stamp = self.get_clock().now().to_msg()
        self.plan_pub.publish(empty)


def main(args=None):
    rclpy.init(args=args)
    node = GoalToPlan()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
