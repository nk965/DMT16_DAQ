from Modules import *

"""
@author: Pike Amornchat, Nicholas Kwok
This thread takes care of all the UART inputs - whether by bluetooth or serial, it will go into a COM port.
The thread reads and decodes the data coming from the MCU into a fully readable string of length 86 (for G
identifiers).

It also deals with connecting to port and provides a method to change port during the execution of the program.
"""


def list_ports():
    """
    Function tries and lists all available ports for connecting
    :return: List of string containing all available COM ports
    """

    # Stack overflowed - makes all 256 possible COM port strings to try,
    # then checks your system to see if this is compatible.
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    # Tries every port in order to see what ports work. If it works, then append to a list and return
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            s.__del__()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class UART:

    def __init__(self, port_name, port='COM7', baud_rate=230400, buffer_size=10000):

        # Attributes for PySerial setup
        self.port = port
        self.baud_rate = baud_rate
        self.buffer_size = buffer_size
        self.UART_buffer = bytearray()
        self.port_name = port_name

        # To store the previous error for comparison so that it doesn't print the same thing too many times.
        self.previous_error = ''

        # Initialize PySerial for both ports - specify baud rate
        self.serial_connection = serial.Serial()

        self.connect_port()

    # Changes the port attribute
    def change_port(self, port):
        """
        Allows the user to change ports with a method
        :param port: string specifying port, e.g. COM9
        :return: None
        """

        self.port = port

    # Resets the UART buffer
    def reset(self):
        """
        Method accessed by Data Manager for full reset - clears buffers
        :return: None
        """

        self.UART_buffer = bytearray()

    # Connect port - used in initialization
    def connect_port(self):
        """
        Tries to connect to the port which is recorded in the class attribute self.port. If unavailable, prints error.
        :return: None
        """

        try:
            # Setup up baud rate and port

            # Choose which port to connect to
            self.serial_connection.port = self.port
            self.serial_connection.baudrate = self.baud_rate

            # Close all and then open the connection
            self.serial_connection.close()
            self.serial_connection.__del__()
            self.serial_connection.open()

            print(f'Successfully connected to {self.port_name} with port {self.port}')

        except Exception as error:

            available_ports = list_ports()

            print('Error in connecting to port : %s' % error)

            print('If your error was the wrong port, try these ports:')

            print(available_ports)

            print(
                'The program is still running but will do nothing until you change the port')

    # To emergency close the port (used for debug)

    def close_port(self):
        """
        Allows the user to close port and terminate the connection - used for debug and reset
        :return: None
        """
        self.serial_connection.close()

    # Run activated by start() method of QThreads
    def send(self, info):
        """
        This module will send out all the configurations to the ports.
        :return: what it sent
        """

        self.serial_connection.write(info)

        time.sleep(0.1)

        print(f'Microcontroller Sends Back: {self.serial_connection.read_all().hex()}')
