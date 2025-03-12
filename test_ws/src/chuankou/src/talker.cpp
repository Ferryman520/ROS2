// talker.cpp
#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <cstdlib> // 用于rand()和srand()
#include <ctime>   // 用于time()
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class MinimalPublisher : public rclcpp::Node {
public:
  MinimalPublisher()
      : Node("minimal_publisher"), count_(0) {
    publisher_ = this->create_publisher<std_msgs::msg::String>("keyboard_input", 10);
    timer_ = this->create_wall_timer(
        1s, std::bind(&MinimalPublisher::timer_callback, this));
    srand(static_cast<unsigned int>(time(nullptr))); // 使用当前时间作为随机种子
  }

private:
  void timer_callback() {
    auto message = std_msgs::msg::String();
    // 随机发送"A"或"B"
    message.data = (rand() % 2 == 0) ? "A" : "B";
    publisher_->publish(message);
    RCLCPP_INFO(this->get_logger(), "Published: %s", message.data.c_str());
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  size_t count_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalPublisher>());
  rclcpp::shutdown();
  return 0;
}
