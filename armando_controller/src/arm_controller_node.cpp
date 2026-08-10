#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joint_state.hpp"

#include <functional>
#include <memory>

class ArmControllerNode : public rclcpp::Node
{
public:
  ArmControllerNode()
  : Node("arm_controller_node")
  {
    RCLCPP_INFO(
      this->get_logger(),
      "Arm controller node started");

    joint_state_subscriber_ =
      this->create_subscription<sensor_msgs::msg::JointState>(
        "/joint_states",
        10,
        std::bind(
          &ArmControllerNode::joint_state_callback,
          this,
          std::placeholders::_1));
  }

private:
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

  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr
    joint_state_subscriber_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  auto node = std::make_shared<ArmControllerNode>();

  rclcpp::spin(node);

  rclcpp::shutdown();

  return 0;
}