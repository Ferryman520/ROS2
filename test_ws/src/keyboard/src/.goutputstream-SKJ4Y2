// keyboard.cpp
#include <iostream> // 包含标准输入输出流库
#include <serial/serial.h> // 包含串行通信库
#include <rclcpp/rclcpp.hpp> // 包含ROS2的C++接口库
#include "std_msgs/msg/string.hpp"//包含 std_msgs 包中的 String 消息类型
#include <termios.h> // 包含终端I/O控制库

serial::Serial ros_ser; // 创建一个串行通信对象

// 定义一个类，继承自rclcpp::Node，用于创建ROS节点
class KeyboardController : public rclcpp::Node {
public:
  // 构造函数，初始化节点名为"keyboard_controller"
  KeyboardController()
      : Node("keyboard_controller") {
    setupSerial(); // 调用setupSerial函数设置串行通信
    publisher_ = this->create_publisher<std_msgs::msg::String>("keyboard_topic", 10); // 创建发布者
  }

  // 设置串行通信参数的函数
  void setupSerial() {
    ros_ser.setPort("/dev/ttyUSB0"); // 设置串行端口为"/dev/ttyUSB0"
    ros_ser.setBaudrate(115200); // 设置波特率为115200
    serial::Timeout to = serial::Timeout::simpleTimeout(1000); // 设置串行通信超时为1000毫秒
    ros_ser.setTimeout(to); // 应用超时设置
    try {//捕获异常行为
      ros_ser.open(); // 尝试打开串行端口
      RCLCPP_INFO(this->get_logger(), "Serial port opened successfully"); // 如果成功，记录日志
    } catch(serial::IOException &e) { // 如果发生异常
      RCLCPP_ERROR(this->get_logger(), "Unable to open serial port"); // 记录错误日志
      rclcpp::shutdown(); // 关闭ROS
      return; // 返回
    }
  }

  // 从键盘读取输入并通过串行端口发送的函数
  void readKeyboard() {
    struct termios orig_termios; // 用于保存原始终端属性的结构体
    tcgetattr(STDIN_FILENO, &orig_termios); // 获取当前终端属性
    struct termios new_termios = orig_termios; // 创建一个新的终端属性结构体并复制原始属性
    new_termios.c_lflag &= ~(ICANON | ECHO); // 修改终端属性，禁用规范输入和回显
    tcsetattr(STDIN_FILENO, TCSANOW, &new_termios); // 应用新的终端属性

    char c; // 用于存储键盘输入的字符变量
    while (rclcpp::ok()) { // 当ROS运行时
      if (read(STDIN_FILENO, &c, 1) == 1) { // 如果从标准输入读取到一个字符
        auto message = std_msgs::msg::String();
        message.data = std::string(1, c); // 将字符转换为字符串
        publisher_->publish(message); // 发布消息
        RCLCPP_INFO(this->get_logger(), "Published to ROS: %c", c); // 记录日志
      }
    }

    tcsetattr(STDIN_FILENO, TCSANOW, &orig_termios); // 恢复原始终端属性
  }

private:
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_; // ROS发布者
  rclcpp::TimerBase::SharedPtr timer_; // ROS定时器，这里未使用
};

// 主函数
int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv); // 初始化ROS
  auto node = std::make_shared<KeyboardController>(); // 创建节点
  std::thread keyboard_thread(&KeyboardController::readKeyboard, node.get()); // 创建一个线程用于读取键盘输入
  keyboard_thread.detach(); // 使线程独立运行
  rclcpp::spin(node); // 保持ROS节点运行
  rclcpp::shutdown(); // 关闭ROS
  ros_ser.close(); // 关闭串行端口
  return 0; // 返回0，表示程序正常退出
}
