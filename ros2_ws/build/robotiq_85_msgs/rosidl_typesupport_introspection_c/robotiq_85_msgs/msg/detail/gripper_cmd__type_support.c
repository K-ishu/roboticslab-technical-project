// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from robotiq_85_msgs:msg/GripperCmd.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "robotiq_85_msgs/msg/detail/gripper_cmd__rosidl_typesupport_introspection_c.h"
#include "robotiq_85_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "robotiq_85_msgs/msg/detail/gripper_cmd__functions.h"
#include "robotiq_85_msgs/msg/detail/gripper_cmd__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  robotiq_85_msgs__msg__GripperCmd__init(message_memory);
}

void robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_fini_function(void * message_memory)
{
  robotiq_85_msgs__msg__GripperCmd__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_message_member_array[6] = {
  {
    "emergency_release",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_85_msgs__msg__GripperCmd, emergency_release),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "emergency_release_dir",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_85_msgs__msg__GripperCmd, emergency_release_dir),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "stop",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_85_msgs__msg__GripperCmd, stop),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_85_msgs__msg__GripperCmd, position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "speed",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_85_msgs__msg__GripperCmd, speed),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "force",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_85_msgs__msg__GripperCmd, force),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_message_members = {
  "robotiq_85_msgs__msg",  // message namespace
  "GripperCmd",  // message name
  6,  // number of fields
  sizeof(robotiq_85_msgs__msg__GripperCmd),
  robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_message_member_array,  // message members
  robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_init_function,  // function to initialize message memory (memory has to be allocated)
  robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_message_type_support_handle = {
  0,
  &robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_robotiq_85_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, robotiq_85_msgs, msg, GripperCmd)() {
  if (!robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_message_type_support_handle.typesupport_identifier) {
    robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &robotiq_85_msgs__msg__GripperCmd__rosidl_typesupport_introspection_c__GripperCmd_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
