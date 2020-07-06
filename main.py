import serial  # For treating with serial connections
import os  # For executing a shell command
import platform  # For getting the operating system name
import time  # For setting the interval of doing pings

param = '-n' if platform.system().lower() == 'windows' else '-c'


def set_controller(controller_ip, serial_1, serial_2):
    """Open the serial ports and
    write the commands to set the controller
    in the Zodiac Fx SDN switch
     """
    try:
        # Open ports serial 1 AND serial 2
        serial_port_1 = serial.Serial(serial_1, 9600)
        serial_port_2 = serial.Serial(serial_2, 9600)

        # Automation for setting de IP of the controller
        serial_port_1.write(b"config \r\n")
        serial_port_2.write(b"config \r\n")
        # Variable to concatenate the IP of the controller
        order = "set of-controller " + controller_ip + " \r\n"
        serial_port_1.write(str.encode(order))
        serial_port_1.write(b"save \r\n")
        serial_port_1.write(b"exit \r\n")
        serial_port_2.write(str.encode(order))
        serial_port_2.write(b"save \r\n")
        serial_port_2.write(b"exit \r\n")
        print("________________________________")
        print("Successfully set controller to IP: " + controller_ip)
        print("________________________________")
        serial_port_1.close()
        serial_port_2.close()
    except serial.SerialException as e:
        # There is no serial port connected
        print("________________________________")
        print("SERIAL PORT EXCEPTION: There is a switch that is not connected")
        print("________________________________")
        exit()
        return None


def is_controller_up(controller):
    """Checks if the controller is up
    by pinging it. If the response is ok returns true
    if its not ok return false
    """
    print("________________________________")
    print("CONNECTION AUTOMATION. PING PROCESS")
    print("________________________________")
    response = os.system("ping " + param + " 1 " + controller)
    # Check the response
    if response == 0:  # Ping is successful
        print("________________________________")
        print("Controller with IP: ", controller, 'is up!')
        return True
    else:
        print("________________________________")
        print("Controller with IP: ", controller, 'is down!')
        return False


def ping_automation_controller(controller_1, controller_2, serial_1, serial_2):
    """Set the controller if it is up, by default if
    both connections are ok the controller set is 10.0.0.20"""

    if is_controller_up(controller_1):
        set_controller(controller_1, serial_1, serial_2)
    else:
        set_controller(controller_2, serial_1, serial_2)


def main():
    """Main function. Automates the process of pinging
    and sleep for 5 seconds before doing the previous stuff again"""

    # Console to enter the values needed

    print("#################################")
    print("SDN CONTROLLER AUTOMATION SCRIPT")
    print("#################################")

    serial_1 = input("Enter serial port nº1: ")  # Set serial 1
    while not serial_1:  # Requests for data until user inputs something
        serial_1 = input("Enter serial port nº1: ")
    print(serial_1.upper().strip() + " set!")

    print("________________________________")

    serial_2 = input("Enter serial port nº2: ")  # Set serial 2
    while not serial_2:  # Requests for data until user inputs something
        serial_2 = input("Enter serial port nº2: ")
    print(serial_2.upper().strip() + " set!")

    print("________________________________")

    controller_1 = input("Enter controller nº1 IP: ")  # Set controller 1 IP
    while not controller_1:  # Requests for data until user inputs something
        controller_1 = input("Enter controller nº1 IP: ")
    print("Controller 1 IP set!")
    print("IP: " + controller_1.strip())

    print("________________________________")

    controller_2 = input("Enter controller nº2 IP: ")  # Set controller 2 IP
    while not controller_2:  # Requests for data until user inputs something
        controller_2 = input("Enter controller nº2 IP: ")
    print("Controller 2 IP set!")
    print("IP: " + controller_2.strip())

    # Infinite while loop
    while True:
        ping_automation_controller(controller_1.strip(), controller_2.strip(),
                                   serial_1.strip().upper(), serial_2.strip().upper())
        print("#################################")
        print("#################################")
        time.sleep(5)


main()
