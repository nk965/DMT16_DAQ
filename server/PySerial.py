from Modules import *


class UART:

    """
    @author: Pike Amornchat
    This thread takes care of all the UART inputs - whether by bluetooth or serial, it will go into a COM port.
    The thread reads and decodes the data coming from the MCU into a fully readable string of length 86 (for G
    identifiers).

    It also deals with connecting to port and provides a method to change port during the execution of the program.
    """

    def __init__(self, DAQ_port='COM14', TB_port='COM10', baud_rate=115200, buffer_size=10000):

        # Attributes for PySerial setup
        self.DAQ_port = DAQ_port
        self.TB_port = TB_port
        self.baud_rate = baud_rate
        self.buffer_size = buffer_size
        self.UART_buffer = bytearray()

        # To store the previous error for comparison so that it doesn't print the same thing too many times.
        self.previous_error = ''

        # Initialize PySerial for both ports - specify baud rate
        self.serial_connection_DAQ = serial.Serial()
        self.serial_connection_TB = serial.Serial()

        # Set the recieve and transmit buffer size
        self.serial_connection_DAQ.set_buffer_size(
            rx_size=self.buffer_size, tx_size=self.buffer_size)
        self.serial_connection_TB.set_buffer_size(
            rx_size=self.buffer_size, tx_size=self.buffer_size)

        # Connect to the COM port for both
        self.connect_port(0)
        self.connect_port(1)

    def list_ports(self):
        """
        Method tries and lists all available ports for connecting
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
    def connect_port(self, portnum):
        """
        Tries to connect to the port which is recorded in the class attribute self.port. If unavailable, prints error.
        :return: None
        """

        try:
            # Setup up baud rate and port

            # Choose which port to connect to
            if portnum == 0:
                self.serial_connection_DAQ.port = self.DAQ_port
                self.serial_connection_DAQ.baudrate = self.baud_rate

                # Close all and then open the connection
                self.serial_connection_DAQ.close()
                self.serial_connection_DAQ.__del__()
                self.serial_connection_DAQ.open()

                print('Successfully connected to DAQ: %s' %
                      self.serial_connection_DAQ.port)

            else:
                self.serial_connection_TB.port = self.TB_port
                self.serial_connection_TB.baudrate = self.baud_rate

                # Close all and then open the connection
                self.serial_connection_TB.close()
                self.serial_connection_TB.__del__()
                self.serial_connection_TB.open()

                print('Successfully connected to Test Bed: %s' %
                      self.serial_connection_TB.port)

        except Exception as error:

            available_ports = self.list_ports()

            if portnum == 0:
                print('Error in connecting to DAQ port : %s' % error)
            else:
                print('Error in connecting to TB port : %s' % error)

            print('If your error was the wrong port, try these ports:')
            print(available_ports)
            print(
                'The program is still running but will do nothing until you change the port')

    # To emergency close the port (used for debug)

    def close_port(self, port):
        """
        Allows the user to close port and terminate the connection - used for debug and reset
        :return: None
        """

        if port == 0:
            self.serial_connection_DAQ.close()
        else:
            self.serial_connection_TB.close()

    # Run activated by start() method of QThreads
    def run(self):
        """
        This module will send out all the configurations to the 2 different ports.
        :return: None
        """

        # Check to see if the connection is open before trying to communicate:
        while self.serial_connection_DAQ.is_open or self.serial_connection_TB.is_open:
            try:

                # Read all data from bytearray - clears buffer too
                data = self.serial_connection.read_all()

                # Check for overflow warning
                if len(data) > 10000:
                    print('WARNING: more than 10000 elements in UART buffer')

                # Adds to the bytearray what we just got from data (extend is like append for bytearray)
                self.UART_buffer.extend(data)

                # Search for '\n' to see the first instance of line break,
                # once found then decode the section found, replacing all commas with spaces, then clears that part of
                # the buffer. Once done, emits using signal to data manager.
                i = self.UART_buffer.find(b'\n')
                if i >= 0:
                    line = self.UART_buffer[:i+1].decode('utf-8').rstrip(',')
                    self.UART_buffer = self.UART_buffer[i+1:]
                    self.serial_to_manager_carrier.emit(line)

                # If there is no error anymore, then reset the previous error so that the exception works again.
                self.previous_error = ''

            # Sometimes the microcontroller has fragments saved, or the user presses soft reset at an awkward time,
            # giving rise to an incomplete line and hence no identifier/incomplete data.
            except Exception as e:

                # Re-initialize the UART buffer
                del self.UART_buffer
                self.UART_buffer = bytearray()

                # If printed the same error already, don't print it again.
                if e == self.previous_error:
                    print(e)
                else:
                    self.previous_error = e