#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import sys, tty, termios, math

STEP = 0.1
KEY_BINDINGS = {
    'q': ( STEP, 0,    0   ),
    'a': (-STEP, 0,    0   ),
    'w': ( 0,    STEP, 0   ),
    's': ( 0,   -STEP, 0   ),
    'e': ( 0,    0,    STEP),
    'd': ( 0,    0,   -STEP),
}
LIMITS = [(-3.14, 3.14), (-1.57, 1.57), (-1.57, 1.57)]

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

class ArmTeleop(Node):
    def __init__(self):
        super().__init__('arm_teleop')
        self.pub = self.create_publisher(
            Float64MultiArray, '/joint_target', 10)
        self.angles = [0.0, 0.0, 0.0]
        self.get_logger().info(
            '\nControls:\n'
            '  Q/A = Base   W/S = Shoulder   E/D = Elbow\n'
            '  R   = Reset    Ctrl+C = Quit\n')

    def run(self):
        while rclpy.ok():
            key = get_key()
            if key == '\x03':
                break
            elif key == 'r':
                self.angles = [0.0, 0.0, 0.0]
                self.get_logger().info('Reset!')
            elif key in KEY_BINDINGS:
                delta = KEY_BINDINGS[key]
                for i in range(3):
                    new = self.angles[i] + delta[i]
                    lo, hi = LIMITS[i]
                    self.angles[i] = max(lo, min(hi, new))
            else:
                continue
            msg = Float64MultiArray()
            msg.data = self.angles
            self.pub.publish(msg)
            print(f'  base:{math.degrees(self.angles[0]):6.1f} '
                  f'shoulder:{math.degrees(self.angles[1]):6.1f} '
                  f'elbow:{math.degrees(self.angles[2]):6.1f} deg',
                  end='\r')

def main(args=None):
    rclpy.init(args=args)
    node = ArmTeleop()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()