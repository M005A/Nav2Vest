import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from sensor_msgs.msg import LaserScan


class ScanGuardrails(Node):
    def __init__(self):
        super().__init__('scan_guardrails')

        # Match pointcloud_to_laserscan / RViz sensor-data QoS
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )

        self.edge_width_rad = 0.12
        self.guardrail_range = 3.3

        self.sub = self.create_subscription(
            LaserScan,
            '/scan_raw',
            self.scan_callback,
            sensor_qos,
        )

        self.pub = self.create_publisher(
            LaserScan,
            '/scan',
            sensor_qos,
        )

        self.get_logger().info('scan_guardrails started: /scan_raw -> /scan with BEST_EFFORT QoS')

    def scan_callback(self, msg: LaserScan):
        out = LaserScan()
        out.header = msg.header
        out.angle_min = msg.angle_min
        out.angle_max = msg.angle_max
        out.angle_increment = msg.angle_increment
        out.time_increment = msg.time_increment
        out.scan_time = msg.scan_time
        out.range_min = msg.range_min
        out.range_max = msg.range_max
        out.intensities = list(msg.intensities)

        ranges = list(msg.ranges)

        for i in range(len(ranges)):
            angle = msg.angle_min + i * msg.angle_increment

            near_left_edge = angle < (msg.angle_min + self.edge_width_rad)
            near_right_edge = angle > (msg.angle_max - self.edge_width_rad)

            if near_left_edge or near_right_edge:
                ranges[i] = min(self.guardrail_range, msg.range_max - 0.05)

        out.ranges = ranges
        self.pub.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = ScanGuardrails()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
