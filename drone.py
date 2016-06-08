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


def drone_hacked(drone):

    data['status'] = 'hacked'
    response = requests.put(host + '/drone/' + drone['id'], data=json.dumps(data), headers=headers)

    if response.status_code in (200, 201):
        return True

    raise Exception


def hacking_in_progress(drone):

    data['status'] = 'in_progress'
    data['mac'] = drone['mac']
    data['channel'] = drone['channel']
    data['client_mac'] = drone['client_mac']
    response = requests.put(host + '/drone/' + drone['id'], data=json.dumps(data), headers=headers)

    if response.status_code in (200, 201):
        return True

    raise Exception


def get_drone_status(drone_id):
    """
    Possible status

    0: Not found
    1: Hacking in progress
    -1: Already hacked

    :param drone_id:
    :return:
    """
    response = requests.get(host + '/drone/' + drone_id)

    if response.status_code == 404:
        return 0

    json_response = response.json()
    if json_response['drone']['status'] == 'hacked':
        return -1

    if json_response['drone']['status'] == 'in_progress':
        return 1


def drone_lost(drone_id):
    response = requests.delete(host + '/drone/' + drone_id)

    if response.status_code == 200:
        return True

    if response.status_code == 404:
        return False

    raise Exception


def log_fail(drone_id):
    drone_lost(drone_id)
    print "UNABLE TO HACK DRONE %s" % drone_id


class DroneLostException(Exception):
    pass