// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robotiq_85_msgs:msg/GripperStat.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__TRAITS_HPP_
#define ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robotiq_85_msgs/msg/detail/gripper_stat__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace robotiq_85_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const GripperStat & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: is_ready
  {
    out << "is_ready: ";
    rosidl_generator_traits::value_to_yaml(msg.is_ready, out);
    out << ", ";
  }

  // member: is_reset
  {
    out << "is_reset: ";
    rosidl_generator_traits::value_to_yaml(msg.is_reset, out);
    out << ", ";
  }

  // member: is_moving
  {
    out << "is_moving: ";
    rosidl_generator_traits::value_to_yaml(msg.is_moving, out);
    out << ", ";
  }

  // member: obj_detected
  {
    out << "obj_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.obj_detected, out);
    out << ", ";
  }

  // member: fault_status
  {
    out << "fault_status: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_status, out);
    out << ", ";
  }

  // member: position
  {
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
    out << ", ";
  }

  // member: requested_position
  {
    out << "requested_position: ";
    rosidl_generator_traits::value_to_yaml(msg.requested_position, out);
    out << ", ";
  }

  // member: current
  {
    out << "current: ";
    rosidl_generator_traits::value_to_yaml(msg.current, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GripperStat & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: is_ready
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_ready: ";
    rosidl_generator_traits::value_to_yaml(msg.is_ready, out);
    out << "\n";
  }

  // member: is_reset
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_reset: ";
    rosidl_generator_traits::value_to_yaml(msg.is_reset, out);
    out << "\n";
  }

  // member: is_moving
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_moving: ";
    rosidl_generator_traits::value_to_yaml(msg.is_moving, out);
    out << "\n";
  }

  // member: obj_detected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "obj_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.obj_detected, out);
    out << "\n";
  }

  // member: fault_status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fault_status: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_status, out);
    out << "\n";
  }

  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
    out << "\n";
  }

  // member: requested_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "requested_position: ";
    rosidl_generator_traits::value_to_yaml(msg.requested_position, out);
    out << "\n";
  }

  // member: current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current: ";
    rosidl_generator_traits::value_to_yaml(msg.current, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GripperStat & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace robotiq_85_msgs

namespace rosidl_generator_traits
{

[[deprecated("use robotiq_85_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robotiq_85_msgs::msg::GripperStat & msg,
  std::ostream & out, size_t indentation = 0)
{
  robotiq_85_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robotiq_85_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const robotiq_85_msgs::msg::GripperStat & msg)
{
  return robotiq_85_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robotiq_85_msgs::msg::GripperStat>()
{
  return "robotiq_85_msgs::msg::GripperStat";
}

template<>
inline const char * name<robotiq_85_msgs::msg::GripperStat>()
{
  return "robotiq_85_msgs/msg/GripperStat";
}

template<>
struct has_fixed_size<robotiq_85_msgs::msg::GripperStat>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<robotiq_85_msgs::msg::GripperStat>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<robotiq_85_msgs::msg::GripperStat>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__TRAITS_HPP_
