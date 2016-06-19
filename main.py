from operator import itemgetter
import sys
import config
import perl
from drone import get_drone_status, hacking_in_progress, drone_hacked, drone_lost,\
    log_fail, DroneLostException, drone_sent_away


def pick_drone(drone_list):

    drones = []
    for drone in drone_list:
        drone_id = drone['DRONE_ID']
        status = get_drone_status(drone_id)
        drones.append({'id': drone_id, 'status': status, 'mac': drone['DRONE_MAC'],
                       'channel': drone['DRONE_CHANNEL']
                          , 'client_mac': drone['CLIENT_MAC']
                       })

    # Remove from list drones already hacked (status == -1)
    drones = [d for d in drones if d['status'] != -1]

    if len(drones) == 0:
        return None

    # Order by status (not detected first, already detected last)
    drones = sorted(drones, key=itemgetter('status'))

    # Return first
    return drones[0]


while True:

    # Monitor and get list of drones detected
    print "monitoring"
    drones_list = perl.monitor()
    print "- monitor finished"
    if len(drones_list) == 0:
        print "-- no drone found"
        continue

    # Pick one drone to hack according to status.
    # If all are already hacked, go back to monitoring
    drone = pick_drone(drones_list)
    if drone is None:
        print "-- no drones to hack"
        continue

    print "-- drone found"
    try:
        # Set status as in_progress
        print "set hacking_in_progress"
        hacking_in_progress(drone)

        count = 3
        while count > 0:
            # Start hacking process
            print "hacking"
            success = perl.hack(drone)
            print "- hacking finished"

            if success:
                # Set status as hacked
                print "- hacking successful: set status hacked"
                drone_hacked(drone)

                # Send drone away
                print "- send drone away"
                perl.send_away()

                # Set status as sent_away
                drone_sent_away(drone)

                # Go back to monitoring
                print "-- back to monitor\n"
                break

            # If not able to hack (but still in range because no Exception catched)
            print "- hacking failed: check status from db"
            status = get_drone_status(drone['id'])  # Re-check status
            if status == -1:  # Hacked by someone else
                print "-- already hacked: back to monitor"
                break  # Go back to monitoring

            print "-- try again"
            count -= 1

        # If not able to hack it after 3 tries: log fail
        if count == 0:
            print "--- tried %d times. Hacking failed" % count
            log_fail(drone['id'])

    except DroneLostException:
        print "ERROR: DRONE LOST"
        drone_lost(drone['id'])