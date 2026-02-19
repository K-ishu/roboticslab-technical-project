// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robotiq_85_msgs:msg/GripperStat.idl
// generated code does not contain a copyright notice
#include "robotiq_85_msgs/msg/detail/gripper_stat__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
robotiq_85_msgs__msg__GripperStat__init(robotiq_85_msgs__msg__GripperStat * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    robotiq_85_msgs__msg__GripperStat__fini(msg);
    return false;
  }
  // is_ready
  // is_reset
  // is_moving
  // obj_detected
  // fault_status
  // position
  // requested_position
  // current
  return true;
}

void
robotiq_85_msgs__msg__GripperStat__fini(robotiq_85_msgs__msg__GripperStat * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // is_ready
  // is_reset
  // is_moving
  // obj_detected
  // fault_status
  // position
  // requested_position
  // current
}

bool
robotiq_85_msgs__msg__GripperStat__are_equal(const robotiq_85_msgs__msg__GripperStat * lhs, const robotiq_85_msgs__msg__GripperStat * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // is_ready
  if (lhs->is_ready != rhs->is_ready) {
    return false;
  }
  // is_reset
  if (lhs->is_reset != rhs->is_reset) {
    return false;
  }
  // is_moving
  if (lhs->is_moving != rhs->is_moving) {
    return false;
  }
  // obj_detected
  if (lhs->obj_detected != rhs->obj_detected) {
    return false;
  }
  // fault_status
  if (lhs->fault_status != rhs->fault_status) {
    return false;
  }
  // position
  if (lhs->position != rhs->position) {
    return false;
  }
  // requested_position
  if (lhs->requested_position != rhs->requested_position) {
    return false;
  }
  // current
  if (lhs->current != rhs->current) {
    return false;
  }
  return true;
}

bool
robotiq_85_msgs__msg__GripperStat__copy(
  const robotiq_85_msgs__msg__GripperStat * input,
  robotiq_85_msgs__msg__GripperStat * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // is_ready
  output->is_ready = input->is_ready;
  // is_reset
  output->is_reset = input->is_reset;
  // is_moving
  output->is_moving = input->is_moving;
  // obj_detected
  output->obj_detected = input->obj_detected;
  // fault_status
  output->fault_status = input->fault_status;
  // position
  output->position = input->position;
  // requested_position
  output->requested_position = input->requested_position;
  // current
  output->current = input->current;
  return true;
}

robotiq_85_msgs__msg__GripperStat *
robotiq_85_msgs__msg__GripperStat__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_85_msgs__msg__GripperStat * msg = (robotiq_85_msgs__msg__GripperStat *)allocator.allocate(sizeof(robotiq_85_msgs__msg__GripperStat), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robotiq_85_msgs__msg__GripperStat));
  bool success = robotiq_85_msgs__msg__GripperStat__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robotiq_85_msgs__msg__GripperStat__destroy(robotiq_85_msgs__msg__GripperStat * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robotiq_85_msgs__msg__GripperStat__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robotiq_85_msgs__msg__GripperStat__Sequence__init(robotiq_85_msgs__msg__GripperStat__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_85_msgs__msg__GripperStat * data = NULL;

  if (size) {
    data = (robotiq_85_msgs__msg__GripperStat *)allocator.zero_allocate(size, sizeof(robotiq_85_msgs__msg__GripperStat), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robotiq_85_msgs__msg__GripperStat__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robotiq_85_msgs__msg__GripperStat__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
robotiq_85_msgs__msg__GripperStat__Sequence__fini(robotiq_85_msgs__msg__GripperStat__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      robotiq_85_msgs__msg__GripperStat__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

robotiq_85_msgs__msg__GripperStat__Sequence *
robotiq_85_msgs__msg__GripperStat__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_85_msgs__msg__GripperStat__Sequence * array = (robotiq_85_msgs__msg__GripperStat__Sequence *)allocator.allocate(sizeof(robotiq_85_msgs__msg__GripperStat__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robotiq_85_msgs__msg__GripperStat__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robotiq_85_msgs__msg__GripperStat__Sequence__destroy(robotiq_85_msgs__msg__GripperStat__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robotiq_85_msgs__msg__GripperStat__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robotiq_85_msgs__msg__GripperStat__Sequence__are_equal(const robotiq_85_msgs__msg__GripperStat__Sequence * lhs, const robotiq_85_msgs__msg__GripperStat__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robotiq_85_msgs__msg__GripperStat__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robotiq_85_msgs__msg__GripperStat__Sequence__copy(
  const robotiq_85_msgs__msg__GripperStat__Sequence * input,
  robotiq_85_msgs__msg__GripperStat__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robotiq_85_msgs__msg__GripperStat);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robotiq_85_msgs__msg__GripperStat * data =
      (robotiq_85_msgs__msg__GripperStat *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robotiq_85_msgs__msg__GripperStat__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robotiq_85_msgs__msg__GripperStat__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robotiq_85_msgs__msg__GripperStat__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
