import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('roboarm')
    rviz_config = os.path.join(pkg, 'config', 'roboarm.rviz')

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        output='screen',
        parameters=[{'use_sim_time': False}]
    )

    return LaunchDescription([rviz])
