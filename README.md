# ROS2
文件“ROS2示例代码”中是ROS2的官方例程
文件“test_ws”是基于ROS2的开发，其中包括摄像头结点，串口结点，键盘结点，urdf对机器人小车建模等

“chuankou”包含一对 ROS2 节点，用于演示如何使用 serial 库进行基本的串口通信集成。这些节点旨在以简单清晰的方式展示如何通过串口发送和接收数据。
项目包含两个主要组件：

talker.cpp：一个发布者节点，会定期在 ROS2 网络上发送随机消息。

listen.cpp：一个订阅者节点，用于监听指定主题上的消息，并集成串口以转发或处理接收到的数据。

“keyboard”提供了一个 ROS2 节点实现，用于捕获键盘输入并将其作为 ROS2 消息发布。此外，它还集成了串口通信，展示了如何处理键盘输入并将其通过串口转发。

keyboard.cpp 文件包含一个名为 KeyboardController 的 ROS2 节点，执行以下任务：

键盘输入捕获：实时读取键盘输入。

ROS2 消息发布：将捕获的键盘输入作为 std_msgs::msg::String 消息发布到名为 keyboard_topic 的 ROS2 主题上。

串口通信：使用 serial 库设置和管理串口连接，允许与外部设备进行通信。

主要功能：

实时键盘输入：无需用户按下回车键即可捕获键盘输入，提供无缝体验。

ROS2 集成：利用 ROS2 主题发布键盘输入，便于与其他 ROS2 节点和系统集成。

串口管理：配置并打开串口（/dev/ttyUSB0，波特率为 115200）以进行通信。

错误处理：正确处理与串口打开相关的错误，并确保在无法打开串口时应用程序能够优雅地关闭。
