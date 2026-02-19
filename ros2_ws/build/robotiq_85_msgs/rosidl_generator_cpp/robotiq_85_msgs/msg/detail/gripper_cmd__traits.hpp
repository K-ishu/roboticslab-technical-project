// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robotiq_85_msgs:msg/GripperCmd.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__TRAITS_HPP_
#define ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robotiq_85_msgs/msg/detail/gripper_cmd__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robotiq_85_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const GripperCmd & msg,
  std::ostream & out)
{
  out << "{";
  // member: emergency_release
  {
    out << "emergency_release: ";
    rosidl_generator_traits::value_to_yaml(msg.emergency_release, out);
    out << ", ";
  }

  // member: emergency_release_dir
  {
    out << "emergency_release_dir: ";
    rosidl_generator_traits::value_to_yaml(msg.emergency_release_dir, out);
    out << ", ";
  }

  // member: stop
  {
    out << "stop: ";
    rosidl_generator_traits::value_to_yaml(msg.stop, out);
    out << ", ";
  }

  // member: position
  {
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
    out << ", ";
  }

  // member: speed
  {
    out << "speed: ";
    rosidl_generator_traits::value_to_yaml(msg.speed, out);
    out << ", ";
  }

  // member: force
  {
    out << "force: ";
    rosidl_generator_traits::value_to_yaml(msg.force, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GripperCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: emergency_release
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "emergency_release: ";
    rosidl_generator_traits::value_to_yaml(msg.emergency_release, out);
    out << "\n";
  }

  // member: emergency_release_dir
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "emergency_release_dir: ";
    rosidl_generator_traits::value_to_yaml(msg.emergency_release_dir, out);
    out << "\n";
  }

  // member: stop
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stop: ";
    rosidl_generator_traits::value_to_yaml(msg.stop, out);
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

  // member: speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "speed: ";
    rosidl_generator_traits::value_to_yaml(msg.speed, out);
    out << "\n";
  }

  // member: force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "force: ";
    rosidl_generator_traits::value_to_yaml(msg.force, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GripperCmd & msg, bool use_flow_style = false)
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
  const robotiq_85_msgs::msg::GripperCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  robotiq_85_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robotiq_85_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const robotiq_85_msgs::msg::GripperCmd & msg)
{
  return robotiq_85_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robotiq_85_msgs::msg::GripperCmd>()
{
  return "robotiq_85_msgs::msg::GripperCmd";
}

template<>
inline const char * name<robotiq_85_msgs::msg::GripperCmd>()
{
  return "robotiq_85_msgs/msg/GripperCmd";
}

template<>
struct has_fixed_size<robotiq_85_msgs::msg::GripperCmd>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<robotiq_85_msgs::msg::GripperCmd>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<robotiq_85_msgs::msg::GripperCmd>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__TRAITS_HPP_
