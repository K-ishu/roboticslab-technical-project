// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from robotiq_85_msgs:msg/GripperStat.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__FUNCTIONS_H_
#define ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "robotiq_85_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "robotiq_85_msgs/msg/detail/gripper_stat__struct.h"

/// Initialize msg/GripperStat message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * robotiq_85_msgs__msg__GripperStat
 * )) before or use
 * robotiq_85_msgs__msg__GripperStat__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
bool
robotiq_85_msgs__msg__GripperStat__init(robotiq_85_msgs__msg__GripperStat * msg);

/// Finalize msg/GripperStat message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
void
robotiq_85_msgs__msg__GripperStat__fini(robotiq_85_msgs__msg__GripperStat * msg);

/// Create msg/GripperStat message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * robotiq_85_msgs__msg__GripperStat__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
robotiq_85_msgs__msg__GripperStat *
robotiq_85_msgs__msg__GripperStat__create();

/// Destroy msg/GripperStat message.
/**
 * It calls
 * robotiq_85_msgs__msg__GripperStat__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
void
robotiq_85_msgs__msg__GripperStat__destroy(robotiq_85_msgs__msg__GripperStat * msg);

/// Check for msg/GripperStat message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
bool
robotiq_85_msgs__msg__GripperStat__are_equal(const robotiq_85_msgs__msg__GripperStat * lhs, const robotiq_85_msgs__msg__GripperStat * rhs);

/// Copy a msg/GripperStat message.
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
robotiq_85_msgs__msg__GripperStat__copy(
  const robotiq_85_msgs__msg__GripperStat * input,
  robotiq_85_msgs__msg__GripperStat * output);

/// Initialize array of msg/GripperStat messages.
/**
 * It allocates the memory for the number of elements and calls
 * robotiq_85_msgs__msg__GripperStat__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
bool
robotiq_85_msgs__msg__GripperStat__Sequence__init(robotiq_85_msgs__msg__GripperStat__Sequence * array, size_t size);

/// Finalize array of msg/GripperStat messages.
/**
 * It calls
 * robotiq_85_msgs__msg__GripperStat__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
void
robotiq_85_msgs__msg__GripperStat__Sequence__fini(robotiq_85_msgs__msg__GripperStat__Sequence * array);

/// Create array of msg/GripperStat messages.
/**
 * It allocates the memory for the array and calls
 * robotiq_85_msgs__msg__GripperStat__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
robotiq_85_msgs__msg__GripperStat__Sequence *
robotiq_85_msgs__msg__GripperStat__Sequence__create(size_t size);

/// Destroy array of msg/GripperStat messages.
/**
 * It calls
 * robotiq_85_msgs__msg__GripperStat__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
void
robotiq_85_msgs__msg__GripperStat__Sequence__destroy(robotiq_85_msgs__msg__GripperStat__Sequence * array);

/// Check for msg/GripperStat message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_85_msgs
bool
robotiq_85_msgs__msg__GripperStat__Sequence__are_equal(const robotiq_85_msgs__msg__GripperStat__Sequence * lhs, const robotiq_85_msgs__msg__GripperStat__Sequence * rhs);

/// Copy an array of msg/GripperStat messages.
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
robotiq_85_msgs__msg__GripperStat__Sequence__copy(
  const robotiq_85_msgs__msg__GripperStat__Sequence * input,
  robotiq_85_msgs__msg__GripperStat__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_85_MSGS__MSG__DETAIL__GRIPPER_STAT__FUNCTIONS_H_
