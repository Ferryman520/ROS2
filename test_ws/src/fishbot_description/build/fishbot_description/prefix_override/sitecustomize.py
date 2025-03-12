import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/potato/test_ws/src/fishbot_description/install/fishbot_description'
