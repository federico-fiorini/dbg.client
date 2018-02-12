## DRONE BE GONE - CLIENT
<br>
Drone Be Gone is a system that creates a no-fly zone where drones cannot enter. Currently works only with Parrot AR.Drones (controlled via wifi).

### HOW IT WORKS
The system works with a certain number of devices (I used Raspberry Pi) disposed on the perimeter of the designed no-fly zone and connected to a central web server that implements a simple REST API and shows logs informations. <br>

[Here](https://github.com/federico-fiorini/dbg.client) there is the implementation of the client application while [this](https://github.com/federico-fiorini/dbg.web-server) is the web server implementation. <br>

The client application detects incoming drones that enter the wifi range of the device, hacks them, takes control and sends the drones away. The following loop is run:<br>

- Monitor<br>
- Detect a drone in the wifi range<br>
- Hack the drone<br>
- Take control<br>
- Turn it to desired direction and send away<br> 
- Go back to monitor mode<br>

An exchange of messages between the devices and the central web server is implemented to set the status of the drones detected and in order for the device to decide if to hack the drone or not (in case another device has already taken control of it).

##### SYSTEM CONFIGURATION
I use a Raspberry Pi with two antennas connected ([Alpha antenna](https://www.amazon.com/Alfa-AWUS036H-802-11b-Wireless-network/dp/B002WCEWU8)) and connected via Ethernet to the local network.
![alt tag](http://i.imgur.com/b9rieBd.png)

Another configuration is possible using one wifi dongle and one antenna. The wifi dongle has a less wide range though.


### HOW IT IS IMPLEMENTED
This project is based on [samyk](https://github.com/samyk) [skyjack](https://github.com/samyk/skyjack) work. It uses similar implementation for the monitoring and hacking parts using [aircrack-ng](http://www.aircrack-ng.org/).<br>
To control the drone it uses [node-ar-drone](https://github.com/felixge/node-ar-drone) library.<br>
The main loop runs in python. 


### DEPENDENCIES

	# Steps for installing aircrack-ng on raspberry pi:
    
    # Start with a updated system:
    sudo apt-get update && sudo apt-get dist-upgrade -y
        
    # Next some requisition:
    sudo apt-get install libnl-dev libssl-dev iw -y
        
    # Get aircrack-ng tar file from site and extract the files
    
    # Go into extracted directory
    make
    sudo make install
    
    # Install Airodump-ng OUI file:
    sudo airodump-ng-oui-update
    
    # Install Node.js:
    curl -sLS https://apt.adafruit.com/add | sudo bash
    sudo apt-get install node
    node -v
        
    # Install AR-Drone:
    npm install ar-drone
    
    # Install requests module for python
    pip install requests

### HOW TO RUN

    # Kill ongoing processes
    sudo airmon-ng check kill
    
    # Set antenna to monitor mode (wifi dongle doesn't support monitor mode,
    # so if you are using 1 antenna and 1 dongle run 'iwconfig' first to check
    # which interface is the antenna)
    sudo airmon-ng start wlan0

    # Set env variables
    export MONITOR_INTERFACE="wlan0mon"
    export DEGREE_DIRECTION="0" # 0 is North, 180 is South, 90 is East, -90 is West
    export WEB_SERVER_HOST="http://192.168.0.3:5000" # If run locally check host from router page and pass port as well
    export DEVICE_ID="RASPBERRY_1"

    # Run main
    python main.py
