// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robotiq_85_msgs:msg/GripperStat.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__STRUCT_H_
#define ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/GripperStat in the package robotiq_85_msgs.
typedef struct robotiq_85_msgs__msg__GripperStat
{
  std_msgs__msg__Header header;
  bool is_ready;
  bool is_reset;
  bool is_moving;
  bool obj_detected;
  uint8_t fault_status;
  float position;
  float requested_position;
  float current;
} robotiq_85_msgs__msg__GripperStat;

// Struct for a sequence of robotiq_85_msgs__msg__GripperStat.
typedef struct robotiq_85_msgs__msg__GripperStat__Sequence
{
  robotiq_85_msgs__msg__GripperStat * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_85_msgs__msg__GripperStat__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__STRUCT_H_
