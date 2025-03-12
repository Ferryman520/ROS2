import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # Set package name and world file path
    package_name = 'fishbot_description'
    world_file_path = 'worlds/neighborhood.world'

    pkg_path = os.path.join(get_package_share_directory(package_name))
    world_path = os.path.join(pkg_path, world_file_path)

    # Spawn position for the robot
    spawn_x_val = '0.0'
    spawn_y_val = '0.0'
    spawn_z_val = '0.0'
    spawn_yaw_val = '0.0'

    # Include the launch file for fishbot
    fishbot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'fishbot_launch.py'
        )]),
        launch_arguments={'use_sim_time': 'true', 'world': world_path}.items()
    )

    # Include Gazebo launch file
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # Publish the robot description
    publish_description = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': os.path.join(pkg_path, 'urdf', 'fishbot_base.urdf')}],
        output='screen'
    )

    # Spawn the entity
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'fishbot', '-file', os.path.join(pkg_path, 'urdf', 'fishbot_base.urdf'),
                   '-x', spawn_x_val,
                   '-y', spawn_y_val,
                   '-z', spawn_z_val,
                   '-Y', spawn_yaw_val],
        output='screen'
    )

    return LaunchDescription([
        fishbot,
        gazebo,
        publish_description,
        spawn_entity,
    ])
