// listen.cpp
#include <functional>
#include <memory>
#include <string>
#include "serial/serial.h"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
using std::placeholders::_1;

serial::Serial ros_ser;

class MinimalSubscriber : public rclcpp::Node {
public:
  MinimalSubscriber()
      : Node("minimal_subscriber") {
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "keyboard_topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
  }

private:
  void topic_callback(const std_msgs::msg::String::SharedPtr msg) const {
    RCLCPP_INFO(this->get_logger(), "Received from keyboard: %s", msg->data.c_str());
    // 这里可以添加处理接收到的键盘信息的代码
  }

  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char *argv[]) {
   rclcpp::init(argc, argv);
  ros_ser.setPort("/dev/ttyUSB0");            //设置端口号
  ros_ser.setBaudrate(115200);                //设置波特率
  serial::Timeout to =serial::Timeout::simpleTimeout(1000);
  ros_ser.setTimeout(to);
  try
  {
    ros_ser.open();
  }
  catch(serial::IOException &e)
  {
    std::cout<<"unable to open"<<std::endl;     //若打开串口失败打印"unable to open"到终端
    return -1;
  }
  if(ros_ser.isOpen())
  {
    std::cout<<"open"<<std::endl;              //若打开串口打印"open"到终端
  }
  else
  {
    return -1;
  }
 
  rclcpp::spin(std::make_shared<MinimalSubscriber>());
  rclcpp::shutdown();
  ros_ser.close();
  return 0;
}
