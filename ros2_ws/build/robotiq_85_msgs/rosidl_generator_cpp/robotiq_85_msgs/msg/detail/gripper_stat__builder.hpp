// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robotiq_85_msgs:msg/GripperStat.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__BUILDER_HPP_
#define ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robotiq_85_msgs/msg/detail/gripper_stat__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robotiq_85_msgs
{

namespace msg
{

namespace builder
{

class Init_GripperStat_current
{
public:
  explicit Init_GripperStat_current(::robotiq_85_msgs::msg::GripperStat & msg)
  : msg_(msg)
  {}
  ::robotiq_85_msgs::msg::GripperStat current(::robotiq_85_msgs::msg::GripperStat::_current_type arg)
  {
    msg_.current = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperStat msg_;
};

class Init_GripperStat_requested_position
{
public:
  explicit Init_GripperStat_requested_position(::robotiq_85_msgs::msg::GripperStat & msg)
  : msg_(msg)
  {}
  Init_GripperStat_current requested_position(::robotiq_85_msgs::msg::GripperStat::_requested_position_type arg)
  {
    msg_.requested_position = std::move(arg);
    return Init_GripperStat_current(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperStat msg_;
};

class Init_GripperStat_position
{
public:
  explicit Init_GripperStat_position(::robotiq_85_msgs::msg::GripperStat & msg)
  : msg_(msg)
  {}
  Init_GripperStat_requested_position position(::robotiq_85_msgs::msg::GripperStat::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_GripperStat_requested_position(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperStat msg_;
};

class Init_GripperStat_fault_status
{
public:
  explicit Init_GripperStat_fault_status(::robotiq_85_msgs::msg::GripperStat & msg)
  : msg_(msg)
  {}
  Init_GripperStat_position fault_status(::robotiq_85_msgs::msg::GripperStat::_fault_status_type arg)
  {
    msg_.fault_status = std::move(arg);
    return Init_GripperStat_position(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperStat msg_;
};

class Init_GripperStat_obj_detected
{
public:
  explicit Init_GripperStat_obj_detected(::robotiq_85_msgs::msg::GripperStat & msg)
  : msg_(msg)
  {}
  Init_GripperStat_fault_status obj_detected(::robotiq_85_msgs::msg::GripperStat::_obj_detected_type arg)
  {
    msg_.obj_detected = std::move(arg);
    return Init_GripperStat_fault_status(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperStat msg_;
};

class Init_GripperStat_is_moving
{
public:
  explicit Init_GripperStat_is_moving(::robotiq_85_msgs::msg::GripperStat & msg)
  : msg_(msg)
  {}
  Init_GripperStat_obj_detected is_moving(::robotiq_85_msgs::msg::GripperStat::_is_moving_type arg)
  {
    msg_.is_moving = std::move(arg);
    return Init_GripperStat_obj_detected(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperStat msg_;
};

class Init_GripperStat_is_reset
{
public:
  explicit Init_GripperStat_is_reset(::robotiq_85_msgs::msg::GripperStat & msg)
  : msg_(msg)
  {}
  Init_GripperStat_is_moving is_reset(::robotiq_85_msgs::msg::GripperStat::_is_reset_type arg)
  {
    msg_.is_reset = std::move(arg);
    return Init_GripperStat_is_moving(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperStat msg_;
};

class Init_GripperStat_is_ready
{
public:
  explicit Init_GripperStat_is_ready(::robotiq_85_msgs::msg::GripperStat & msg)
  : msg_(msg)
  {}
  Init_GripperStat_is_reset is_ready(::robotiq_85_msgs::msg::GripperStat::_is_ready_type arg)
  {
    msg_.is_ready = std::move(arg);
    return Init_GripperStat_is_reset(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperStat msg_;
};

class Init_GripperStat_header
{
public:
  Init_GripperStat_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperStat_is_ready header(::robotiq_85_msgs::msg::GripperStat::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_GripperStat_is_ready(msg_);
  }

private:
  ::robotiq_85_msgs::msg::GripperStat msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_85_msgs::msg::GripperStat>()
{
  return robotiq_85_msgs::msg::builder::Init_GripperStat_header();
}

}  // namespace robotiq_85_msgs

#endif  // ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__BUILDER_HPP_
