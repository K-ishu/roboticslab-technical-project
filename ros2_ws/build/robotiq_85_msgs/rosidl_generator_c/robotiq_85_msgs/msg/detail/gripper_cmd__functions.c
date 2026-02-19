// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robotiq_85_msgs:msg/GripperCmd.idl
// generated code does not contain a copyright notice
#include "robotiq_85_msgs/msg/detail/gripper_cmd__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
robotiq_85_msgs__msg__GripperCmd__init(robotiq_85_msgs__msg__GripperCmd * msg)
{
  if (!msg) {
    return false;
  }
  // emergency_release
  // emergency_release_dir
  // stop
  // position
  // speed
  // force
  return true;
}

void
robotiq_85_msgs__msg__GripperCmd__fini(robotiq_85_msgs__msg__GripperCmd * msg)
{
  if (!msg) {
    return;
  }
  // emergency_release
  // emergency_release_dir
  // stop
  // position
  // speed
  // force
}

bool
robotiq_85_msgs__msg__GripperCmd__are_equal(const robotiq_85_msgs__msg__GripperCmd * lhs, const robotiq_85_msgs__msg__GripperCmd * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // emergency_release
  if (lhs->emergency_release != rhs->emergency_release) {
    return false;
  }
  // emergency_release_dir
  if (lhs->emergency_release_dir != rhs->emergency_release_dir) {
    return false;
  }
  // stop
  if (lhs->stop != rhs->stop) {
    return false;
  }
  // position
  if (lhs->position != rhs->position) {
    return false;
  }
  // speed
  if (lhs->speed != rhs->speed) {
    return false;
  }
  // force
  if (lhs->force != rhs->force) {
    return false;
  }
  return true;
}

bool
robotiq_85_msgs__msg__GripperCmd__copy(
  const robotiq_85_msgs__msg__GripperCmd * input,
  robotiq_85_msgs__msg__GripperCmd * output)
{
  if (!input || !output) {
    return false;
  }
  // emergency_release
  output->emergency_release = input->emergency_release;
  // emergency_release_dir
  output->emergency_release_dir = input->emergency_release_dir;
  // stop
  output->stop = input->stop;
  // position
  output->position = input->position;
  // speed
  output->speed = input->speed;
  // force
  output->force = input->force;
  return true;
}

robotiq_85_msgs__msg__GripperCmd *
robotiq_85_msgs__msg__GripperCmd__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_85_msgs__msg__GripperCmd * msg = (robotiq_85_msgs__msg__GripperCmd *)allocator.allocate(sizeof(robotiq_85_msgs__msg__GripperCmd), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robotiq_85_msgs__msg__GripperCmd));
  bool success = robotiq_85_msgs__msg__GripperCmd__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robotiq_85_msgs__msg__GripperCmd__destroy(robotiq_85_msgs__msg__GripperCmd * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robotiq_85_msgs__msg__GripperCmd__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robotiq_85_msgs__msg__GripperCmd__Sequence__init(robotiq_85_msgs__msg__GripperCmd__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_85_msgs__msg__GripperCmd * data = NULL;

  if (size) {
    data = (robotiq_85_msgs__msg__GripperCmd *)allocator.zero_allocate(size, sizeof(robotiq_85_msgs__msg__GripperCmd), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robotiq_85_msgs__msg__GripperCmd__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robotiq_85_msgs__msg__GripperCmd__fini(&data[i - 1]);
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
robotiq_85_msgs__msg__GripperCmd__Sequence__fini(robotiq_85_msgs__msg__GripperCmd__Sequence * array)
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
      robotiq_85_msgs__msg__GripperCmd__fini(&array->data[i]);
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

robotiq_85_msgs__msg__GripperCmd__Sequence *
robotiq_85_msgs__msg__GripperCmd__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_85_msgs__msg__GripperCmd__Sequence * array = (robotiq_85_msgs__msg__GripperCmd__Sequence *)allocator.allocate(sizeof(robotiq_85_msgs__msg__GripperCmd__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robotiq_85_msgs__msg__GripperCmd__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robotiq_85_msgs__msg__GripperCmd__Sequence__destroy(robotiq_85_msgs__msg__GripperCmd__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robotiq_85_msgs__msg__GripperCmd__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robotiq_85_msgs__msg__GripperCmd__Sequence__are_equal(const robotiq_85_msgs__msg__GripperCmd__Sequence * lhs, const robotiq_85_msgs__msg__GripperCmd__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robotiq_85_msgs__msg__GripperCmd__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robotiq_85_msgs__msg__GripperCmd__Sequence__copy(
  const robotiq_85_msgs__msg__GripperCmd__Sequence * input,
  robotiq_85_msgs__msg__GripperCmd__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robotiq_85_msgs__msg__GripperCmd);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robotiq_85_msgs__msg__GripperCmd * data =
      (robotiq_85_msgs__msg__GripperCmd *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robotiq_85_msgs__msg__GripperCmd__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robotiq_85_msgs__msg__GripperCmd__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robotiq_85_msgs__msg__GripperCmd__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
