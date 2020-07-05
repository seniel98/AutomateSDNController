import serial  # For treating with serial connections
import os  # For executing a shell command
import platform  # For getting the operating system name
import time  # For setting the interval of doing pings

param = '-n' if platform.system().lower() == 'windows' else '-c'


def set_controller(controller_ip):
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


def ping_automation_controller_1():
    hostname = "10.0.0.20 "  # example

    response = os.system("ping " + param + " 1 " + hostname)

    # and then check the response...
    if response == 0:
        print(hostname, 'is up!')
    else:
        print(hostname, 'is down!')
        set_controller("10.0.0.30")


def ping_automation_controller_2():
    hostname = "10.0.0.30 "  # example

    response = os.system("ping " + param + " 1 " + hostname)

    # and then check the response...
    if response == 0:
        print(hostname, 'is up!')
    else:
        print(hostname, 'is down!')
        set_controller("10.0.0.20")


ping_automation_controller_1()
