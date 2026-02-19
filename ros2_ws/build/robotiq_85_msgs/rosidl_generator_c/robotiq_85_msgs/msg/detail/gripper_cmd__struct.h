// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robotiq_85_msgs:msg/GripperCmd.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__STRUCT_H_
#define ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/GripperCmd in the package robotiq_85_msgs.
typedef struct robotiq_85_msgs__msg__GripperCmd
{
  bool emergency_release;
  uint32_t emergency_release_dir;
  bool stop;
  float position;
  float speed;
  float force;
} robotiq_85_msgs__msg__GripperCmd;

// Struct for a sequence of robotiq_85_msgs__msg__GripperCmd.
typedef struct robotiq_85_msgs__msg__GripperCmd__Sequence
{
  robotiq_85_msgs__msg__GripperCmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_85_msgs__msg__GripperCmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__STRUCT_H_
