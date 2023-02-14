"""
@author: Nicholas Kwok
Main script for communicating with microcontrollers
"""

import time

from PySerial import UART 
from server_config import inputInfo

def float_to_byte(value: float, info: dict) -> tuple:

    min_input, max_input = info["range"][0], info["range"][1]
    
    max_output = 2**info["bits"] - 1

    scaled = (value - min_input) / (max_input - min_input) * (max_output)

    rounded = round(scaled)

    byte_count = info["bits"] // 8
    byte_array = bytearray(value.to_bytes(byte_count, byteorder='big'))

    actual = (rounded * (max_input - min_input)) / max_output + min_input # check if this is correct
    
    return actual, byte_array

def STBCommand(testDelay: float): 

    # TODO finish STB Command 

    time.sleep(testDelay)

    return {"Testbed Delay": testDelay}

def SDAQCommand(UART: object, PIVfreq_val: float, Datafreq_val: float, PIVfreq_info: dict, Datafreq_info: dict):

    UART.connect_port(0) # Connect through UART to DAQ (port 0 i.e., COM14)
    
    message = bytearray.fromhex('01') # Command specific hex identifier - check documentation for details

    actualPIV, outPIVfreq = float_to_byte(PIVfreq_val, PIVfreq_info)

    actualDatafreq, outDatafreq = float_to_byte(Datafreq_val, Datafreq_info)

    message.extend(outPIVfreq + outDatafreq)

    UART.send(message)

    return {"Logger Frequency": actualDatafreq, "PIV Frequency": actualPIV} 

if __name__ == "__main__":

    '''
    FOR TESTING ONLY -  in the future, a function will be called from this script in server.py

    TODO code functionality to use default values in a "debug" mode
    
    '''

    status = {}

    # start communication process by initialising UART class

    process = UART(DAQ_port='COM9')

    '''
    
    status["STB"] = STBCommand()
    
    '''

    status['SDAQ'] = SDAQCommand(process, inputInfo["PIVfreq"]["defaultValue"], inputInfo["Datafreq"]["defaultValue"], inputInfo["PIVfreq"], inputInfo["Datafreq"]) # TODO replace the second and third arguments with actual values from user input

    print(status)