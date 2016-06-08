import subprocess


def monitor():
    pipe = subprocess.Popen(["perl", "bin/monitor.pl", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

