// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robotiq_85_msgs:msg/GripperStat.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__STRUCT_HPP_
#define ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__robotiq_85_msgs__msg__GripperStat __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_85_msgs__msg__GripperStat __declspec(deprecated)
#endif

namespace robotiq_85_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct GripperStat_
{
  using Type = GripperStat_<ContainerAllocator>;

  explicit GripperStat_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_ready = false;
      this->is_reset = false;
      this->is_moving = false;
      this->obj_detected = false;
      this->fault_status = 0;
      this->position = 0.0f;
      this->requested_position = 0.0f;
      this->current = 0.0f;
    }
  }

  explicit GripperStat_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_ready = false;
      this->is_reset = false;
      this->is_moving = false;
      this->obj_detected = false;
      this->fault_status = 0;
      this->position = 0.0f;
      this->requested_position = 0.0f;
      this->current = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _is_ready_type =
    bool;
  _is_ready_type is_ready;
  using _is_reset_type =
    bool;
  _is_reset_type is_reset;
  using _is_moving_type =
    bool;
  _is_moving_type is_moving;
  using _obj_detected_type =
    bool;
  _obj_detected_type obj_detected;
  using _fault_status_type =
    uint8_t;
  _fault_status_type fault_status;
  using _position_type =
    float;
  _position_type position;
  using _requested_position_type =
    float;
  _requested_position_type requested_position;
  using _current_type =
    float;
  _current_type current;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__is_ready(
    const bool & _arg)
  {
    this->is_ready = _arg;
    return *this;
  }
  Type & set__is_reset(
    const bool & _arg)
  {
    this->is_reset = _arg;
    return *this;
  }
  Type & set__is_moving(
    const bool & _arg)
  {
    this->is_moving = _arg;
    return *this;
  }
  Type & set__obj_detected(
    const bool & _arg)
  {
    this->obj_detected = _arg;
    return *this;
  }
  Type & set__fault_status(
    const uint8_t & _arg)
  {
    this->fault_status = _arg;
    return *this;
  }
  Type & set__position(
    const float & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__requested_position(
    const float & _arg)
  {
    this->requested_position = _arg;
    return *this;
  }
  Type & set__current(
    const float & _arg)
  {
    this->current = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robotiq_85_msgs::msg::GripperStat_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_85_msgs::msg::GripperStat_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_85_msgs::msg::GripperStat_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_85_msgs::msg::GripperStat_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_85_msgs::msg::GripperStat_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_85_msgs::msg::GripperStat_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_85_msgs::msg::GripperStat_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_85_msgs::msg::GripperStat_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_85_msgs::msg::GripperStat_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_85_msgs::msg::GripperStat_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_85_msgs__msg__GripperStat
    std::shared_ptr<robotiq_85_msgs::msg::GripperStat_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_85_msgs__msg__GripperStat
    std::shared_ptr<robotiq_85_msgs::msg::GripperStat_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GripperStat_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->is_ready != other.is_ready) {
      return false;
    }
    if (this->is_reset != other.is_reset) {
      return false;
    }
    if (this->is_moving != other.is_moving) {
      return false;
    }
    if (this->obj_detected != other.obj_detected) {
      return false;
    }
    if (this->fault_status != other.fault_status) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    if (this->requested_position != other.requested_position) {
      return false;
    }
    if (this->current != other.current) {
      return false;
    }
    return true;
  }
  bool operator!=(const GripperStat_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GripperStat_

// alias to use template instance with default allocator
using GripperStat =
  robotiq_85_msgs::msg::GripperStat_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robotiq_85_msgs

#endif  // ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__STRUCT_HPP_
