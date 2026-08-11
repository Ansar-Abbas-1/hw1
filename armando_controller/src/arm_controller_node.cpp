#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"
#include "trajectory_msgs/msg/joint_trajectory.hpp"
#include "trajectory_msgs/msg/joint_trajectory_point.hpp"

#include <functional>
#include <memory>
#include <vector>
#include <chrono>
#include <string>

class ArmControllerNode : public rclcpp::Node
{
public:
  ArmControllerNode()
  : Node("arm_controller_node")
  {
    RCLCPP_INFO(
      this->get_logger(),
      "Arm controller node started");

    // ---------------------------------------------------------
    //  Read the selected control mode
    // ---------------------------------------------------------

    this->declare_parameter<std::string>("control_mode", "position");

    control_mode_ =
      this->get_parameter("control_mode").as_string();

    RCLCPP_INFO(
      this->get_logger(),
      "Control mode: %s",
      control_mode_.c_str());


    // ---------------------------------------------------------
    // Subscriber to the current joint states
    // ---------------------------------------------------------

    joint_state_subscriber_ =
      this->create_subscription<sensor_msgs::msg::JointState>(
        "/joint_states",
        10,
        std::bind(
          &ArmControllerNode::joint_state_callback,
          this,
          std::placeholders::_1));


    // ---------------------------------------------------------
    // Position controller publisher
    // ---------------------------------------------------------

    position_publisher_ =
      this->create_publisher<std_msgs::msg::Float64MultiArray>(
        "/position_controller/commands",
        10);


    // ---------------------------------------------------------
    // Joint trajectory controller publisher
    // ---------------------------------------------------------

    trajectory_publisher_ =
      this->create_publisher<trajectory_msgs::msg::JointTrajectory>(
        "/trajectory_controller/joint_trajectory",
        10);


    // ---------------------------------------------------------
    // Timer for sending commands sequentially
    // ---------------------------------------------------------

    command_timer_ =
      this->create_wall_timer(
        std::chrono::seconds(3),
        std::bind(
          &ArmControllerNode::send_command,
          this));
  }


private:

  // ---------------------------------------------------------
  // Callback for receiving joint states
  // ---------------------------------------------------------

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


  // ---------------------------------------------------------
  // Select position or trajectory command
  // ---------------------------------------------------------

  void send_command()
  {
    if (control_mode_ == "position")
    {
      send_position_command();
    }
    else if (control_mode_ == "trajectory")
    {
      send_trajectory_command();
    }
    else
    {
      RCLCPP_ERROR(
        this->get_logger(),
        "Invalid control_mode: %s",
        control_mode_.c_str());

      command_timer_->cancel();
    }
  }


  // ---------------------------------------------------------
  // Position controller command
  // ---------------------------------------------------------

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

      default:
        command_timer_->cancel();
        return;
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


  // ---------------------------------------------------------
  // Joint trajectory controller command
  // ---------------------------------------------------------

  void send_trajectory_command()
  {
    trajectory_msgs::msg::JointTrajectory trajectory;

    // Joint names must match the robot joints
    trajectory.joint_names = {
      "j0",
      "j1",
      "j2",
      "j3"
    };


    trajectory_msgs::msg::JointTrajectoryPoint point;


    switch (command_index_)
    {
      case 0:
        point.positions = {
          0.0, 0.0, 0.0, 0.0
        };
        break;

      case 1:
        point.positions = {
          0.4, 0.0, 0.0, 0.0
        };
        break;

      case 2:
        point.positions = {
          0.4, 0.4, 0.0, 0.0
        };
        break;

      case 3:
        point.positions = {
          0.0, 0.0, 0.4, 0.0
        };
        break;

      default:
        command_timer_->cancel();
        return;
    }


    // The trajectory should reach the requested
    // position one second after the command is sent.
    point.time_from_start.sec = 1;


    trajectory.points.push_back(point);


    trajectory_publisher_->publish(trajectory);


    RCLCPP_INFO(
      this->get_logger(),
      "Published trajectory command %zu",
      command_index_ + 1);


    command_index_++;


    // Stop after four commands
    if (command_index_ >= 4)
    {
      command_timer_->cancel();
    }
  }


  // ---------------------------------------------------------
  // ROS interfaces
  // ---------------------------------------------------------

  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr
    joint_state_subscriber_;

  rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr
    position_publisher_;

  rclcpp::Publisher<trajectory_msgs::msg::JointTrajectory>::SharedPtr
    trajectory_publisher_;

  rclcpp::TimerBase::SharedPtr
    command_timer_;


  // ---------------------------------------------------------
  //  Selected control mode
  // ---------------------------------------------------------

  std::string control_mode_;


  // Command counter
  size_t command_index_ = 0;
};


int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  auto node =
    std::make_shared<ArmControllerNode>();

  rclcpp::spin(node);

  rclcpp::shutdown();

  return 0;
}
