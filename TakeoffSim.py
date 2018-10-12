from dronekit import connect, VehicleMode, LocationGlobalRelative
import dronekit_sitl
import time

"""
Function that sets the drone to Loiter mode
(mode that holds altitude and current position),
and attempts to arm it.
"""
def setupDrone(currentDrone):

    #Sets the drone to GUIDED mode
    print("\nSetting drone to GUIDED mode now...")
    currentDrone.mode = VehicleMode("GUIDED")
    print("Drone is in GUIDED mode.")

    #Arm the drone
    print("\nDrone is armable. Arming it now...")
    currentDrone.armed = True
    time.sleep(2)

    #If the drone does not successfully arm,
    #attempt to arm it again.
    while not currentDrone.armed:
        print("--Drone is still arming...")
        currentDrone.armed = True
        time.sleep(2)

    print("\nDrone is armed!")

"""
Function that checks the current drone's altitude and prints it every second.
Once its target altitude is reached, print it.
"""
def altitudeCheck(currentDrone, targetAltitude):

    print("Taking off now.")
    # While the target altitude has yet to be reached, print the drone's
    # current altitude every couple of seconds.
    while currentDrone.location.global_relative_frame.alt < (targetAltitude - 0.1):
        print " Altitude: ", currentDrone.location.global_relative_frame.alt
        time.sleep(1)

    # Once the target altitude is reached, print it.
    print("--Target Altitude of " + str(targetAltitude) + "m reached.")

def main():
    #Have the Pi connect to the pixhawk through Telem 2
    print("Attempting to connect to drone...")
    drone = connect('udp:127.0.0.1:1231', wait_ready=True)

    #When the Pi successfully connects to the Pixhawk,
    #run the setupDrone function.
    print("\nDrone is connected, setting up now...")
    setupDrone(drone)

    #Variable that stores the altitude (in meters)
    #at which the drone should hover at.
    targetAltitude = 5.0
    print("Target altitude of " + str(targetAltitude) + "m has been set.")

    #Have drone takeoff at targeted height
    drone.simple_takeoff(targetAltitude)

    #Run function to check the drone's current altitude
    altitudeCheck(drone, targetAltitude)

    #Override the throttle channel before
    #switching to Position Hold mode
    drone.channels.overrides['3'] = 1500

    #Switch to Position Hold mode
    print("\nSetting mode to PosHold now.")
    drone.mode = VehicleMode("POSHOLD")
    print("\nDrone is in PosHold mode")

    #Drone hovers for 10 seconds before landing
    print("\n10 seconds until land")
    time.sleep(10)
    drone.mode = VehicleMode('LAND')
    print("\nLanding Now.")
    
    drone.close()

main()
