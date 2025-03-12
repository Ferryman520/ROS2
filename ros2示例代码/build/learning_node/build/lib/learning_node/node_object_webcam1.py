#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2节点示例-通过摄像头识别检测图片中出现的人并描边
"""

import rclpy                            # ROS2 Python接口库
from rclpy.node import Node             # ROS2 节点类

import cv2                              # OpenCV图像处理库
import numpy as np                      # Python数值计算库

# 人的皮肤颜色HSV阈值下限和上限
lower_skin1 = np.array([0, 48, 20])
upper_skin1 = np.array([20, 255, 255])
lower_skin2 = np.array([150, 48, 20])
upper_skin2 = np.array([180, 255, 255])

def object_detect(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 图像从BGR颜色模型转换为HSV模型

    # 根据皮肤颜色的两个范围创建掩膜
    mask_skin1 = cv2.inRange(hsv_img, lower_skin1, upper_skin1)
    mask_skin2 = cv2.inRange(hsv_img, lower_skin2, upper_skin2)
    mask_skin = cv2.bitwise_or(mask_skin1, mask_skin2)  # 合并两个掩膜

    # 图像二值化
    mask_skin = cv2.medianBlur(mask_skin, 5)  # 使用中值滤波器减少噪声
    contours, hierarchy = cv2.findContours(mask_skin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # 图像中轮廓检测

    for cnt in contours:  # 去除一些轮廓面积太小的噪声
        if cv2.contourArea(cnt) < 500:
            continue

        (x, y, w, h) = cv2.boundingRect(cnt)  # 得到轮廓的左上角xy像素坐标及轮廓范围的宽和高
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)  # 将轮廓勾勒出来

    cv2.imshow("object", image)  # 使用OpenCV显示处理后的图像效果
    cv2.waitKey(50)

def main(args=None):  # ROS2节点主入口main函数
    rclpy.init(args=args)  # ROS2 Python接口初始化
    node = Node("node_object_webcam")  # 创建ROS2节点对象并进行初始化
    node.get_logger().info("ROS2节点示例：检测图像中的人并描边")

    cap = cv2.VideoCapture(0)

    while rclpy.ok():
        ret, image = cap.read()  # 读取一帧图像
        if ret == True:
            object_detect(image)  # 人检测

    node.destroy_node()  # 销毁节点对象
    cap.release()  # 释放摄像头资源
    cv2.destroyAllWindows()  # 关闭所有OpenCV窗口
    rclpy.shutdown()  # 关闭ROS2 Python接口

if __name__ == '__main__':
    main()
