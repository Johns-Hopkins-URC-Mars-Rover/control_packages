from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    package_name = 'rover_description'
    urdf_name = 'rover.urdf'

    package_share = get_package_share_directory(package_name)

    urdf_file = os.path.join(
        package_share, 'urdf', urdf_name
    )

    controller_config = os.path.join(
        package_share, 'config', 'rover_controller.yaml'
    )

    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

    return LaunchDescription([
        # Publish the robot description and TF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description
            }],
            output='screen'
        ),

        # Start ROS 2 Control and initialize hardware
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[controller_config],
            remappings=[
                ('~/robot_description', '/robot_description'),
                ('robot_description', '/robot_description')
            ],
            output='screen'
        ),

        # Publish actual joint state feedback
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster'],
            output='screen'
        ),

        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['diff_drive_controller'],
            output='screen'
        ),

        # Visualize the rover
        Node(
            package='rviz2',
            executable='rviz2',
            output='screen'
        ),
    ])
