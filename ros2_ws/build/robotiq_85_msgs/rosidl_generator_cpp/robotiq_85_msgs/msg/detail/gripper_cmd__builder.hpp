// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robotiq_85_msgs:msg/GripperCmd.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__BUILDER_HPP_
#define ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robotiq_85_msgs/msg/detail/gripper_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robotiq_85_msgs
{

namespace msg
{

namespace builder
{

class Init_GripperCmd_force
{
public:
  explicit Init_GripperCmd_force(::robotiq_85_msgs::msg::GripperCmd & msg)
  : msg_(msg)
  {}
  ::robotiq_85_msgs::msg::GripperCmd force(::robotiq_85_msgs::msg::GripperCmd::_force_type arg)
  {
    msg_.force = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperCmd msg_;
};

class Init_GripperCmd_speed
{
public:
  explicit Init_GripperCmd_speed(::robotiq_85_msgs::msg::GripperCmd & msg)
  : msg_(msg)
  {}
  Init_GripperCmd_force speed(::robotiq_85_msgs::msg::GripperCmd::_speed_type arg)
  {
    msg_.speed = std::move(arg);
    return Init_GripperCmd_force(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperCmd msg_;
};

class Init_GripperCmd_position
{
public:
  explicit Init_GripperCmd_position(::robotiq_85_msgs::msg::GripperCmd & msg)
  : msg_(msg)
  {}
  Init_GripperCmd_speed position(::robotiq_85_msgs::msg::GripperCmd::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_GripperCmd_speed(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperCmd msg_;
};

class Init_GripperCmd_stop
{
public:
  explicit Init_GripperCmd_stop(::robotiq_85_msgs::msg::GripperCmd & msg)
  : msg_(msg)
  {}
  Init_GripperCmd_position stop(::robotiq_85_msgs::msg::GripperCmd::_stop_type arg)
  {
    msg_.stop = std::move(arg);
    return Init_GripperCmd_position(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperCmd msg_;
};

class Init_GripperCmd_emergency_release_dir
{
public:
  explicit Init_GripperCmd_emergency_release_dir(::robotiq_85_msgs::msg::GripperCmd & msg)
  : msg_(msg)
  {}
  Init_GripperCmd_stop emergency_release_dir(::robotiq_85_msgs::msg::GripperCmd::_emergency_release_dir_type arg)
  {
    msg_.emergency_release_dir = std::move(arg);
    return Init_GripperCmd_stop(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperCmd msg_;
};

class Init_GripperCmd_emergency_release
{
public:
  Init_GripperCmd_emergency_release()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperCmd_emergency_release_dir emergency_release(::robotiq_85_msgs::msg::GripperCmd::_emergency_release_type arg)
  {
    msg_.emergency_release = std::move(arg);
    return Init_GripperCmd_emergency_release_dir(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperCmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_85_msgs::msg::GripperCmd>()
{
  return robotiq_85_msgs::msg::builder::Init_GripperCmd_emergency_release();
}

}  // namespace robotiq_85_msgs

#endif  // ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__BUILDER_HPP_
