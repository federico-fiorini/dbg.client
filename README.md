##DRONE BE GONE - CLIENT

###HOW TO RUN

    # Check which interface is the antenna
    iwconfig

    # Set env variable
    export MONITOR_INTERFACE="interface [wlan0mon or wlan1mon]"

    # Kill some processes that might interfere with airmon-ng
    sudo airmon-ng check kill

    # Run passing device_id and web server host and port
    python main.py RASPBERRY_ID http://192.168.0.101:5000
