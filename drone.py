import requests
import config
import json

host = config.WEB_SERVER_HOST
headers = {
    'Content-Type': 'application/json'
}

data = {
    'device_id': config.DEVICE_ID
}


def drone_hacked(drone, count=0):

    data['status'] = 'hacked'

    try:
        response = requests.put(host + '/drone/' + drone['id'], data=json.dumps(data), headers=headers, timeout=1)

        if response.status_code in (200, 201):
            return True

        return False

    except requests.exceptions.Timeout:

        if count == 2:
            return False

        drone_hacked(drone, count + 1)


def drone_sent_away(drone, count=0):

    data['status'] = 'sent_away'

    try:
        response = requests.put(host + '/drone/' + drone['id'], data=json.dumps(data), headers=headers, timeout=1)

        if response.status_code in (200, 201):
            return True

        return False

    except requests.exceptions.Timeout:

        if count == 2:
            return False

        drone_sent_away(drone, count + 1)


def hacking_in_progress(drone, count=0):

    data['status'] = 'in_progress'
    data['mac'] = drone['mac']
    data['channel'] = drone['channel']
    data['client_mac'] = drone['client_mac']

    try:
        response = requests.put(host + '/drone/' + drone['id'], data=json.dumps(data), headers=headers, timeout=1)

        if response.status_code in (200, 201):
            return True

        return False

    except requests.exceptions.Timeout:

        if count == 2:
            return False

        hacking_in_progress(drone, count + 1)


def get_drone_status(drone_id, count=0):
    """
    Possible status

    0: Needs to be hacked
    1: Hacking in progress
    -1: Already hacked

    :param drone_id:
    :return:
    """

    try:
        response = requests.get(host + '/drone/' + drone_id, timeout=1)

        if response.status_code == 404:
            return 0

        json_response = response.json()

        if json_response['drone']['status'] == 'lost':
            return 0

        if json_response['drone']['status'] == 'hack_failed':
            return 0

        if json_response['drone']['status'] == 'hacked':
            return -1

        if json_response['drone']['status'] == 'sent_away':
            return 1

        if json_response['drone']['status'] == 'in_progress':
            return 1

    except requests.exceptions.Timeout:

        if count == 2:
            return False

        get_drone_status(drone_id, count + 1)


def drone_lost(drone_id, count=0):

    data['status'] = 'lost'

    try:
        response = requests.put(host + '/drone/' + drone_id, data=json.dumps(data), headers=headers)

        if response.status_code in (200, 201):
            return True

        return False

    except requests.exceptions.Timeout:

        if count == 2:
            return False

        drone_lost(drone_id, count + 1)


def log_fail(drone_id, count=0):
    print "UNABLE TO HACK DRONE %s" % drone_id

    data['status'] = 'hack_failed'

    try:
        response = requests.put(host + '/drone/' + drone_id, data=json.dumps(data), headers=headers)

        if response.status_code in (200, 201):
            return True

        return False

    except requests.exceptions.Timeout:

        if count == 2:
            return False

        log_fail(drone_id, count + 1)


class DroneLostException(Exception):
    pass