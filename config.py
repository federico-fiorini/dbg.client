import os

WEB_SERVER_HOST = os.environ.get('WEB_SERVER_HOST', 'http://127.0.0.1:5000')
DEVICE_ID = os.environ.get('DEVICE_ID', 'UKNOWN_DEVICE')
MONITOR_INTERFACE = os.environ.get('MONITOR_INTERFACE', 'wlan1mon')
DEGREE_DIRECTION = os.environ.get('DEGREE_DIRECTION', '0')
