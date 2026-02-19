import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/kishu/roboticslab-technical-project/ros2_ws/install/robotiq_85_driver'
