# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robotiq_85_msgs:msg/GripperCmd.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GripperCmd(type):
    """Metaclass of message 'GripperCmd'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('robotiq_85_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'robotiq_85_msgs.msg.GripperCmd')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__gripper_cmd
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__gripper_cmd
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__gripper_cmd
            cls._TYPE_SUPPORT = module.type_support_msg__msg__gripper_cmd
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__gripper_cmd

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GripperCmd(metaclass=Metaclass_GripperCmd):
    """Message class 'GripperCmd'."""

    __slots__ = [
        '_emergency_release',
        '_emergency_release_dir',
        '_stop',
        '_position',
        '_speed',
        '_force',
    ]

    _fields_and_field_types = {
        'emergency_release': 'boolean',
        'emergency_release_dir': 'uint32',
        'stop': 'boolean',
        'position': 'float',
        'speed': 'float',
        'force': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.emergency_release = kwargs.get('emergency_release', bool())
        self.emergency_release_dir = kwargs.get('emergency_release_dir', int())
        self.stop = kwargs.get('stop', bool())
        self.position = kwargs.get('position', float())
        self.speed = kwargs.get('speed', float())
        self.force = kwargs.get('force', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.emergency_release != other.emergency_release:
            return False
        if self.emergency_release_dir != other.emergency_release_dir:
            return False
        if self.stop != other.stop:
            return False
        if self.position != other.position:
            return False
        if self.speed != other.speed:
            return False
        if self.force != other.force:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def emergency_release(self):
        """Message field 'emergency_release'."""
        return self._emergency_release

    @emergency_release.setter
    def emergency_release(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'emergency_release' field must be of type 'bool'"
        self._emergency_release = value

    @builtins.property
    def emergency_release_dir(self):
        """Message field 'emergency_release_dir'."""
        return self._emergency_release_dir

    @emergency_release_dir.setter
    def emergency_release_dir(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'emergency_release_dir' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'emergency_release_dir' field must be an unsigned integer in [0, 4294967295]"
        self._emergency_release_dir = value

    @builtins.property
    def stop(self):
        """Message field 'stop'."""
        return self._stop

    @stop.setter
    def stop(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'stop' field must be of type 'bool'"
        self._stop = value

    @builtins.property
    def position(self):
        """Message field 'position'."""
        return self._position

    @position.setter
    def position(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'position' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'position' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._position = value

    @builtins.property
    def speed(self):
        """Message field 'speed'."""
        return self._speed

    @speed.setter
    def speed(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'speed' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'speed' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._speed = value

    @builtins.property
    def force(self):
        """Message field 'force'."""
        return self._force

    @force.setter
    def force(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'force' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'force' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._force = value
