# 导入必要的模块和类
import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

# 定义生成launch描述的函数
def generate_launch_description():
    # 定义包名和URDF文件名
    package_name = 'urdf'
    urdf_name = "fishbot_base.urdf"

    # 创建LaunchDescription对象
    ld = LaunchDescription()
    # 使用FindPackageShare查找包的共享路径
    pkg_share = FindPackageShare(package=package_name).find(package_name) 
    # 构造URDF文件的完整路径
    urdf_model_path = os.path.join(pkg_share, f'urdf/{urdf_name}')

    # 创建robot_state_publisher节点，用于发布机器人状态
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_model_path]  # 传递URDF文件路径作为参数
        )

    # 创建joint_state_publisher_gui节点，用于发布关节状态
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        arguments=[urdf_model_path]  # 传递URDF文件路径作为参数
        )

    # 创建rviz2节点，用于可视化
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',  # 在屏幕上显示输出
        )

    # 将节点添加到launch描述中
    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(rviz2_node)

    # 返回生成的launch描述对象
    return ld
