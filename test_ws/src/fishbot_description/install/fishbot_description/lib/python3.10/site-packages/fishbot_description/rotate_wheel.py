#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import threading
import time

class RotateWheelNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info(f"node {name} init..")

        # 定义四个轮子速度参数
        self.declare_parameter('front_left_wheel_speed', 0.0)
        self.declare_parameter('front_right_wheel_speed', 0.0)
        self.declare_parameter('back_left_wheel_speed', 0.0)
        self.declare_parameter('back_right_wheel_speed', 0.0)

        # 创建并初始化发布者成员属性 pub_joint_states_
        self.joint_states_publisher_ = self.create_publisher(JointState, "joint_states", 10)
        # 初始化数据
        self._init_joint_states()
        # 设置 Rate 频率
        self.pub_rate = self.create_rate(30)
        # 创建线程
        self.thread_ = threading.Thread(target=self._thread_pub)
        # 开始线程
        self.thread_.start()

    def _init_joint_states(self):
        # 初始化 jonit_states 话题对象
        self.joint_states = JointState()
        # 设置 header
        self.joint_states.header.stamp = self.get_clock().now().to_msg()
        self.joint_states.header.frame_id = ""
        # 关节名称
        self.joint_states.name = ['front_left_wheel_joint', 'front_right_wheel_joint', 'back_left_wheel_joint', 'back_right_wheel_joint']
        # 关节的位置
        self.joint_states.position = [0.0, 0.0, 0.0, 0.0]
        # 初始四个轮子的速度
        self.joint_speeds = [0.0, 0.0, 0.0, 0.0]

        # 使用参数进行赋值，通过 rqt 工具设置参数的值以此控制轮子的速度
        self.joint_states.velocity = [
            self.get_parameter('front_left_wheel_speed').value,
            self.get_parameter('front_right_wheel_speed').value,
            self.get_parameter('back_left_wheel_speed').value,
            self.get_parameter('back_right_wheel_speed').value
        ]

        # 力
        self.joint_states.effort = []

    # 设置四个关节速度
    def update_speed(self, speeds):
        self.joint_speeds = speeds

    # 创建线程
    def _thread_pub(self):
        last_update_time = time.time()
        while rclpy.ok():
            # 一个更新周期，即前面设置的 rate：1/30 s
            delta_time = time.time() - last_update_time
            last_update_time = time.time()
            # 更新位置
            for i in range(4):
                self.joint_states.position[i] += delta_time * self.joint_states.velocity[i]

            # 更新速度
            self.joint_states.velocity = [
                self.get_parameter('front_left_wheel_speed').value,
                self.get_parameter('front_right_wheel_speed').value,
                self.get_parameter('back_left_wheel_speed').value,
                self.get_parameter('back_right_wheel_speed').value
            ]

            # 更新 header
            self.joint_states.header.stamp = self.get_clock().now().to_msg()
            # 发布关节数据
            self.joint_states_publisher_.publish(self.joint_states)
            self.pub_rate.sleep()

def main(args=None):
    rclpy.init(args=args)
    node = RotateWheelNode("rotate_fishbot_wheel")
    # 示例速度设置，可以根据实际需求调整
    # node.update_speed([10.0, -10.0, 10.0, -10.0])
    rclpy.spin(node)
    rclpy.shutdown()
