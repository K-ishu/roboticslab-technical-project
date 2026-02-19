// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robotiq_85_msgs:msg/GripperCmd.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__STRUCT_HPP_
#define ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robotiq_85_msgs__msg__GripperCmd __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_85_msgs__msg__GripperCmd __declspec(deprecated)
#endif

namespace robotiq_85_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct GripperCmd_
{
  using Type = GripperCmd_<ContainerAllocator>;

  explicit GripperCmd_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->emergency_release = false;
      this->emergency_release_dir = 0ul;
      this->stop = false;
      this->position = 0.0f;
      this->speed = 0.0f;
      this->force = 0.0f;
    }
  }

  explicit GripperCmd_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->emergency_release = false;
      this->emergency_release_dir = 0ul;
      this->stop = false;
      this->position = 0.0f;
      this->speed = 0.0f;
      this->force = 0.0f;
    }
  }

  // field types and members
  using _emergency_release_type =
    bool;
  _emergency_release_type emergency_release;
  using _emergency_release_dir_type =
    uint32_t;
  _emergency_release_dir_type emergency_release_dir;
  using _stop_type =
    bool;
  _stop_type stop;
  using _position_type =
    float;
  _position_type position;
  using _speed_type =
    float;
  _speed_type speed;
  using _force_type =
    float;
  _force_type force;

  // setters for named parameter idiom
  Type & set__emergency_release(
    const bool & _arg)
  {
    this->emergency_release = _arg;
    return *this;
  }
  Type & set__emergency_release_dir(
    const uint32_t & _arg)
  {
    this->emergency_release_dir = _arg;
    return *this;
  }
  Type & set__stop(
    const bool & _arg)
  {
    this->stop = _arg;
    return *this;
  }
  Type & set__position(
    const float & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__speed(
    const float & _arg)
  {
    this->speed = _arg;
    return *this;
  }
  Type & set__force(
    const float & _arg)
  {
    this->force = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_85_msgs__msg__GripperCmd
    std::shared_ptr<robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_85_msgs__msg__GripperCmd
    std::shared_ptr<robotiq_85_msgs::msg::GripperCmd_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GripperCmd_ & other) const
  {
    if (this->emergency_release != other.emergency_release) {
      return false;
    }
    if (this->emergency_release_dir != other.emergency_release_dir) {
      return false;
    }
    if (this->stop != other.stop) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    if (this->speed != other.speed) {
      return false;
    }
    if (this->force != other.force) {
      return false;
    }
    return true;
  }
  bool operator!=(const GripperCmd_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GripperCmd_

// alias to use template instance with default allocator
using GripperCmd =
  robotiq_85_msgs::msg::GripperCmd_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robotiq_85_msgs

#endif  // ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__STRUCT_HPP_
