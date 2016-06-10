import subprocess
import config


def monitor():
    pipe = subprocess.Popen(["perl", "bin/monitor.pl", config.MONITOR_INTERFACE.replace('mon', ''), config.MONITOR_INTERFACE],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = pipe.communicate()

    label = []
    drones = []
    output_lines = stdout_data.splitlines()
    for line in output_lines:
        if line.startswith("LABEL"):
            label = line.split('|')[1:]

        if line.startswith("DATA"):
            data = line.split('|')[1:]
            drone = {label[i]: v for i, v in enumerate(data)}
            drones.append(drone)

    return drones


def hack(drone):

    # Determine interfaces name
    if config.MONITOR_INTERFACE == "wlan0mon":
        interface = "wlan1"
    else:
        interface = "wlan0"

    pipe = subprocess.Popen(["perl", "bin/hack.pl", drone['id'], drone['mac'], drone['channel'], drone['client_mac'],
                             config.MONITOR_INTERFACE, interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = pipe.communicate()
    return True


def send_away():
    pipe = subprocess.Popen(["node", "bin/send_away.js"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = pipe.communicate()
