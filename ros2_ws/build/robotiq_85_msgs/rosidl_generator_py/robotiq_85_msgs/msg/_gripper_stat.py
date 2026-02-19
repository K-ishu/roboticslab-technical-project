# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robotiq_85_msgs:msg/GripperStat.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GripperStat(type):
    """Metaclass of message 'GripperStat'."""

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
                'robotiq_85_msgs.msg.GripperStat')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__gripper_stat
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__gripper_stat
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__gripper_stat
            cls._TYPE_SUPPORT = module.type_support_msg__msg__gripper_stat
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__gripper_stat

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GripperStat(metaclass=Metaclass_GripperStat):
    """Message class 'GripperStat'."""

    __slots__ = [
        '_header',
        '_is_ready',
        '_is_reset',
        '_is_moving',
        '_obj_detected',
        '_fault_status',
        '_position',
        '_requested_position',
        '_current',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'is_ready': 'boolean',
        'is_reset': 'boolean',
        'is_moving': 'boolean',
        'obj_detected': 'boolean',
        'fault_status': 'uint8',
        'position': 'float',
        'requested_position': 'float',
        'current': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.is_ready = kwargs.get('is_ready', bool())
        self.is_reset = kwargs.get('is_reset', bool())
        self.is_moving = kwargs.get('is_moving', bool())
        self.obj_detected = kwargs.get('obj_detected', bool())
        self.fault_status = kwargs.get('fault_status', int())
        self.position = kwargs.get('position', float())
        self.requested_position = kwargs.get('requested_position', float())
        self.current = kwargs.get('current', float())

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
        if self.header != other.header:
            return False
        if self.is_ready != other.is_ready:
            return False
        if self.is_reset != other.is_reset:
            return False
        if self.is_moving != other.is_moving:
            return False
        if self.obj_detected != other.obj_detected:
            return False
        if self.fault_status != other.fault_status:
            return False
        if self.position != other.position:
            return False
        if self.requested_position != other.requested_position:
            return False
        if self.current != other.current:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def is_ready(self):
        """Message field 'is_ready'."""
        return self._is_ready

    @is_ready.setter
    def is_ready(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_ready' field must be of type 'bool'"
        self._is_ready = value

    @builtins.property
    def is_reset(self):
        """Message field 'is_reset'."""
        return self._is_reset

    @is_reset.setter
    def is_reset(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_reset' field must be of type 'bool'"
        self._is_reset = value

    @builtins.property
    def is_moving(self):
        """Message field 'is_moving'."""
        return self._is_moving

    @is_moving.setter
    def is_moving(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_moving' field must be of type 'bool'"
        self._is_moving = value

    @builtins.property
    def obj_detected(self):
        """Message field 'obj_detected'."""
        return self._obj_detected

    @obj_detected.setter
    def obj_detected(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'obj_detected' field must be of type 'bool'"
        self._obj_detected = value

    @builtins.property
    def fault_status(self):
        """Message field 'fault_status'."""
        return self._fault_status

    @fault_status.setter
    def fault_status(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'fault_status' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'fault_status' field must be an unsigned integer in [0, 255]"
        self._fault_status = value

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
    def requested_position(self):
        """Message field 'requested_position'."""
        return self._requested_position

    @requested_position.setter
    def requested_position(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'requested_position' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'requested_position' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._requested_position = value

    @builtins.property
    def current(self):
        """Message field 'current'."""
        return self._current

    @current.setter
    def current(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'current' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'current' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._current = value
