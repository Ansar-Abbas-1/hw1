#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"

#include <functional>
#include <memory>
#include <vector>
#include <chrono>

class ArmControllerNode : public rclcpp::Node
{
public:
  ArmControllerNode()
  : Node("arm_controller_node")
  {
    RCLCPP_INFO(
      this->get_logger(),
      "Arm controller node started");

    // Subscriber to the current joint states
    joint_state_subscriber_ =
      this->create_subscription<sensor_msgs::msg::JointState>(
        "/joint_states",
        10,
        std::bind(
          &ArmControllerNode::joint_state_callback,
          this,
          std::placeholders::_1));

    // Publisher for joint position commands
    position_publisher_ =
      this->create_publisher<std_msgs::msg::Float64MultiArray>(
        "/position_controller/commands",
        10);

    // Timer for sending commands sequentially
    command_timer_ =
      this->create_wall_timer(
        std::chrono::seconds(3),
        std::bind(
          &ArmControllerNode::send_position_command,
          this));
  }

private:

  //  Callback for receiving joint states
  void joint_state_callback(
    const sensor_msgs::msg::JointState::SharedPtr msg)
  {
    for (size_t i = 0; i < msg->name.size(); ++i)
    {
      RCLCPP_INFO(
        this->get_logger(),
        "Joint: %s, Position: %.3f rad",
        msg->name[i].c_str(),
        msg->position[i]);
    }
  }

  // Q4(c): Send four different position commands
  void send_position_command()
  {
    std_msgs::msg::Float64MultiArray command;

    switch (command_index_)
    {
      case 0:
        command.data = {0.0, 0.0, 0.0, 0.0};
        break;

      case 1:
        command.data = {0.4, 0.0, 0.0, 0.0};
        break;

      case 2:
        command.data = {0.4, 0.4, 0.0, 0.0};
        break;

      case 3:
        command.data = {0.0, 0.0, 0.4, 0.0};
        break;
    }

    position_publisher_->publish(command);

    RCLCPP_INFO(
      this->get_logger(),
      "Published position command %zu",
      command_index_ + 1);

    command_index_++;

    // Stop after four commands
    if (command_index_ >= 4)
    {
      command_timer_->cancel();
    }
  }

  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr
    joint_state_subscriber_;

  rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr
    position_publisher_;

  rclcpp::TimerBase::SharedPtr
    command_timer_;

  size_t command_index_ = 0;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);


  auto node = std::make_shared<ArmControllerNode>();

  rclcpp::spin(node);

  rclcpp::shutdown();

  return 0;
}