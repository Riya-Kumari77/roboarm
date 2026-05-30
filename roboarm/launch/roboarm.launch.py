import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    pkg = get_package_share_directory('roboarm')
    urdf_file  = os.path.join(pkg, 'urdf', 'roboarm.urdf.xacro')
    robot_desc = xacro.process_file(urdf_file).toxml()
    world_file = os.path.join(pkg, 'worlds', 'arm_world.sdf')

    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_file],
        output='screen'
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True
        }]
    )

    spawn = TimerAction(
        period=2.0,
        actions=[Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-name', 'roboarm',
                       '-topic', 'robot_description',
                       '-z', '0.05'],
            output='screen'
        )]
    )

    controller = TimerAction(
        period=3.0,
        actions=[Node(
            package='roboarm',
            executable='arm_controller',
            output='screen',
            parameters=[{'use_sim_time': True}]
        )]
    )

    return LaunchDescription([gazebo, rsp, spawn, controller])