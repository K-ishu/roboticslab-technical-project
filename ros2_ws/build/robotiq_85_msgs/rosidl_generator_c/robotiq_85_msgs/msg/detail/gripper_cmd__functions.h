// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from robotiq_85_msgs:msg/GripperCmd.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__FUNCTIONS_H_
#define ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "robotiq_85_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "robotiq_85_msgs/msg/detail/gripper_cmd__struct.h"

/// Initialize msg/GripperCmd message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * robotiq_85_msgs__msg__GripperCmd
 * )) before or use
 * robotiq_85_msgs__msg__GripperCmd__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
bool
robotiq_85_msgs__msg__GripperCmd__init(robotiq_85_msgs__msg__GripperCmd * msg);

/// Finalize msg/GripperCmd message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
void
robotiq_85_msgs__msg__GripperCmd__fini(robotiq_85_msgs__msg__GripperCmd * msg);

/// Create msg/GripperCmd message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * robotiq_85_msgs__msg__GripperCmd__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
robotiq_85_msgs__msg__GripperCmd *
robotiq_85_msgs__msg__GripperCmd__create();

/// Destroy msg/GripperCmd message.
/**
 * It calls
 * robotiq_85_msgs__msg__GripperCmd__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
void
robotiq_85_msgs__msg__GripperCmd__destroy(robotiq_85_msgs__msg__GripperCmd * msg);

/// Check for msg/GripperCmd message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
bool
robotiq_85_msgs__msg__GripperCmd__are_equal(const robotiq_85_msgs__msg__GripperCmd * lhs, const robotiq_85_msgs__msg__GripperCmd * rhs);

/// Copy a msg/GripperCmd message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
bool
robotiq_85_msgs__msg__GripperCmd__copy(
  const robotiq_85_msgs__msg__GripperCmd * input,
  robotiq_85_msgs__msg__GripperCmd * output);

/// Initialize array of msg/GripperCmd messages.
/**
 * It allocates the memory for the number of elements and calls
 * robotiq_85_msgs__msg__GripperCmd__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
bool
robotiq_85_msgs__msg__GripperCmd__Sequence__init(robotiq_85_msgs__msg__GripperCmd__Sequence * array, size_t size);

/// Finalize array of msg/GripperCmd messages.
/**
 * It calls
 * robotiq_85_msgs__msg__GripperCmd__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
void
robotiq_85_msgs__msg__GripperCmd__Sequence__fini(robotiq_85_msgs__msg__GripperCmd__Sequence * array);

/// Create array of msg/GripperCmd messages.
/**
 * It allocates the memory for the array and calls
 * robotiq_85_msgs__msg__GripperCmd__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
robotiq_85_msgs__msg__GripperCmd__Sequence *
robotiq_85_msgs__msg__GripperCmd__Sequence__create(size_t size);

/// Destroy array of msg/GripperCmd messages.
/**
 * It calls
 * robotiq_85_msgs__msg__GripperCmd__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
void
robotiq_85_msgs__msg__GripperCmd__Sequence__destroy(robotiq_85_msgs__msg__GripperCmd__Sequence * array);

/// Check for msg/GripperCmd message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
bool
robotiq_85_msgs__msg__GripperCmd__Sequence__are_equal(const robotiq_85_msgs__msg__GripperCmd__Sequence * lhs, const robotiq_85_msgs__msg__GripperCmd__Sequence * rhs);

/// Copy an array of msg/GripperCmd messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
bool
robotiq_85_msgs__msg__GripperCmd__Sequence__copy(
  const robotiq_85_msgs__msg__GripperCmd__Sequence * input,
  robotiq_85_msgs__msg__GripperCmd__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_CMD__FUNCTIONS_H_
