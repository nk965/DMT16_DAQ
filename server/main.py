"""
@author: Nicholas Kwok, Pike Amornchat
Main script for communicating with microcontrollers
hello
"""

import time

from PySerial import UART, list_ports
from server_config import inputInfo

import numpy as np


def base_15_protocol_convert(num):

    def numberToBase(n, b):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        return digits[::-1]

    bases = {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "10": "A",
        "11": "B",
        "12": "C",
        "13": "D",
        "14": "E",
        "15": "F"
    }

    # Temporary array converted to base 15 in numbers
    temp = numberToBase(num, 15)
    final = ""  # The send string

    for i in range(len(temp) - 1, -1, -2):  # Add 1 to pad to hex
        temp[i] = temp[i] + 1

    for i in temp:  # Convert to hex string + concatenate
        final = final + bases[str(i)]

    if len(final) % 2 == 1:  # Pad 0 if need be
        final = "0" + final

    return final


def convert_frequency_to_clock_tick(input_freq):

    prescaler = 332  # Hardcoded prescaler - numerically optimized by Desmos
    clock_speed = 84*10**6  # STM32F407 TIM6 clock speed
    # The number of ticks converted into an integer
    no_ticks = int(np.round(clock_speed/(prescaler*input_freq)))
    # The actual frequency using the number of ticks
    actual_freq = clock_speed/(prescaler*no_ticks)

    hex_ticks = base_15_protocol_convert(no_ticks)

    return actual_freq, hex_ticks


def float_to_hex_string(value: float, info: dict) -> tuple:

    min_input, max_input = info["range"][0], info["range"][1]

    max_output = 15**(info["bits"] // 4) - 1

    min_output = 0

    scaled = (((value - min_input) / (max_input - min_input))
              * (max_output - min_output)) + min_output

    rounded = round(scaled)

    actual = (((rounded - min_output) * (max_input - min_input)) /
              (max_output - min_output)) + min_input

    return actual, base_15_protocol_convert(rounded)


def STBCommand(testDelay: float):

    # TODO finish STB Command

    time.sleep(testDelay)

    return {"Testbed Delay": testDelay}


def ETB1Command(UART):

    message = bytearray.fromhex("09")

    read_receipt = UART.send(message)

    return {"ETB1 Output": read_receipt}


def ETB2Command(UART):

    message = bytearray.fromhex("0A")

    read_receipt = UART.send(message)

    return {"ETB2 Output": read_receipt}


def EDAQCommand(UART):

    message = bytearray.fromhex("0B010101")

    print(f'EDAQ Sends: 0B010101')

    print(message)

    UART.close_port()  # Close UART to DAQ Microcontroller (port 0)

    return {"EDAQ Output": read_receipt}


def SDAQCommand(UART: object, PIVfreq_val: float, Datafreq_val: float, LenExp_val: float, PIVfreq_info: dict, Datafreq_info: dict, LenExp_info: dict):

    UART.connect_port()  # Connect through UART to DAQ (port 0)

    hex_identifier = "03"  # Command specific hex identifier - check documentation for detail

    actualPIV, outPIVticks = convert_frequency_to_clock_tick(PIVfreq_val)

    actualDatafreq, outDatafreq = float_to_hex_string(
        Datafreq_val, Datafreq_info)
    
    actualLenExp, outLenExp = float_to_hex_string(
        LenExp_val, LenExp_info)

    message = bytearray.fromhex(hex_identifier + outPIVticks + outDatafreq + outLenExp + "0101")

    UART.send(message)

    return {"Logger Frequency": actualDatafreq, "PIV Frequency": actualPIV, "PIV Ticks": outPIVticks, "Experiment Length": actualLenExp}

def SDAQ2Command(UART, LenExperiment, LenExperimentInfo):

    hex_identifier = "0F"

    actualLen, outLen = float_to_hex_string(LenExperiment, LenExperimentInfo)

    print(f'SDAQ2 Sends: {hex_identifier} {outLen} 01')

    message = bytearray.fromhex(hex_identifier + outLen + "01")

    UART.send(0, message)

    return {"Length of Experiment": actualLen}


if __name__ == "__main__":

    '''
    FOR TESTING ONLY -  in the future, a function will be called from this script in server.py

    TODO code functionality to use default values in a "debug" mode

    '''

    status = {}

    ports_available = list_ports()

    DAQ_UART = UART("DAQ Microcontroller", ports_available[1]) # check this, optionally, specify the port number

    # status["STB"] = STBCommand()

    status['SDAQ'] = SDAQCommand(DAQ_UART, 10, inputInfo["Datafreq"]["defaultValue"],
                                 inputInfo["PIVfreq"], inputInfo["Datafreq"])  # TODO replace the second and third arguments with actual values from user input

    status['SDAQ2'] = SDAQ2Command(DAQ_UART, inputInfo["lenExperiment"]['defaultValue'], inputInfo["lenExperiment"])

    time.sleep(0.1)
    
    # status['EBT1'] = ETB1Command(process)

    time.sleep(3)

    status['SDAQ'] = SDAQCommand(DAQ_UART, 5, inputInfo["Datafreq"]["defaultValue"],
                                 inputInfo["PIVfreq"], inputInfo["Datafreq"])

    # status['EBT2'] = ETB2Command(TB_UART)

    status['EDAQ'] = EDAQCommand(DAQ_UART)

    print(status)
