#include "rclcpp/rclcpp.hpp"

class ArmControllerNode : public rclcpp::Node
{
public:
    ArmControllerNode()
    : Node("arm_controller_node")
    {
        RCLCPP_INFO(this->get_logger(), "Arm controller node started");
    }
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<ArmControllerNode>();

    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}
