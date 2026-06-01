#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
import math


class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')

        self.joint_pub = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )
        self.gz_joint_pubs = [
            self.create_publisher(
                Float64,
                '/model/roboarm/joint/base_joint/cmd_pos',
                10
            ),
            self.create_publisher(
                Float64,
                '/model/roboarm/joint/shoulder_joint/cmd_pos',
                10
            ),
            self.create_publisher(
                Float64,
                '/model/roboarm/joint/elbow_joint/cmd_pos',
                10
            ),
        ]

        self.target_sub = self.create_subscription(
            Float64MultiArray,
            '/joint_target',
            self.target_callback,
            10
        )

        self.angles = [0.0, 0.0, 0.0]
        self.joint_names = [
            'base_joint',
            'shoulder_joint',
            'elbow_joint'
        ]

        self.timer = self.create_timer(
            0.02,
            self.publish_joints
        )

        self.get_logger().info(
            'RoboArm Controller started!'
        )

    def target_callback(self, msg):
        if len(msg.data) == 3:
            self.angles = list(msg.data)

            self.get_logger().info(
                f'Moving -> '
                f'base:{math.degrees(self.angles[0]):.1f} '
                f'shoulder:{math.degrees(self.angles[1]):.1f} '
                f'elbow:{math.degrees(self.angles[2]):.1f} deg'
            )

    def publish_joints(self):
        try:
            msg = JointState()

            msg.header.stamp = (
                self.get_clock().now().to_msg()
            )

            msg.name = self.joint_names
            msg.position = self.angles
            msg.velocity = [0.0, 0.0, 0.0]
            msg.effort = [0.0, 0.0, 0.0]

            self.joint_pub.publish(msg)

            for pub, angle in zip(self.gz_joint_pubs, self.angles):
                cmd = Float64()
                cmd.data = angle
                pub.publish(cmd)

        except Exception as e:
            print("ERROR IN publish_joints:", e)


def main(args=None):
    rclpy.init(args=args)

    node = ArmController()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info(
            'Shutting down.'
        )

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
