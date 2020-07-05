import serial  # For treating with serial connections
import os  # For executing a shell command
import platform  # For getting the operating system name
import time  # For setting the interval of doing pings

param = '-n' if platform.system().lower() == 'windows' else '-c'


def set_controller(controller_ip):
    """Open the serial ports and
    write the commands to set the controller
    in the Zodiac Fx SDN switch
     """
    try:
        # Open ports COM3 AND COM4
        com3 = serial.Serial("COM3", 9600)
        # com4 = serial.Serial("COM4", 9600)

        # Automation for setting de IP of the controller
        com3.write(b"config \r\n")
        # Variable to concatenate the IP of the controller
        order = "set of-controller " + controller_ip + " \r\n"
        com3.write(str.encode(order))
        com3.write(b"save \r\n")
        com3.write(b"exit \r\n")
        print("Successfully set controller to IP: " + controller_ip)
        com3.close()
    except serial.SerialException as e:
        # There is no serial port connected
        print("There is a switch that is not connected")
        return None


def is_controller_up(controller):
    """Checks if the controller is up
    by pinging it. If the response is ok returns true
    if its not ok return false
    """
    response = os.system("ping " + param + " 1 " + controller)
    # Check the response
    if response == 0:  # Ping is successful
        print(controller, 'is up!')
        return True
    else:
        print(controller, 'is down!')
        return False


def ping_automation_controller(controller_1, controller_2):
    """Set the controller if it is up, by default if
    both connections are ok the controller set is 10.0.0.20"""
    if is_controller_up(controller_1):
        set_controller(controller_1)
    else:
        set_controller(controller_2)


def main():
    """Main function. Automates the process of pinging
    and sleep for 5 seconds before doing the previous stuff again"""
    while True:
        ping_automation_controller("10.0.0.20", "10.0.0.30")
        time.sleep(5)


main()
