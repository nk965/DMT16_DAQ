"""
@author: Nicholas Kwok, Pike Amornchat
List of commands from Central PC side
"""

from Modules import *

from helpers import convert_frequency_to_clock_tick, float_to_hex_string

def TBTesting(UART):

    message = bytearray.fromhex("FF") # initial testing
    
    result = UART.send(message)

    return {"TB Testing": result}

def DyeInjectTest(UART):

    message = "turn 10"

    result = UART.send(message.encode("ascii"))

    return {"Dye Injection Output": result}


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

    UART.send(message)  

    UART.close_port()  # Close UART to DAQ Microcontroller (port 0)

    return {"EDAQ Output": message}


def SDAQCommand(UART: object, PIVfreq_val: float, Datafreq_val: float, PIVfreq_info: dict, Datafreq_info: dict):

    hex_identifier = "03"  # Command specific hex identifier - check documentation for detail

    actualPIV, outPIVticks = convert_frequency_to_clock_tick(PIVfreq_val)

    actualDatafreq, outDatafreq = float_to_hex_string(
        Datafreq_val, Datafreq_info)
    
    print(f'SDAQ Sends: {hex_identifier} {outPIVticks} {outDatafreq}')

    message = bytearray.fromhex(hex_identifier + outPIVticks + outDatafreq)

    UART.send(message)

    return {"Logger Frequency": actualDatafreq, "PIV Frequency": actualPIV, "PIV Ticks": outPIVticks}

def SDAQ2Command(UART, LenExperiment, LenExperimentInfo):

    hex_identifier = "0F"

    actualLen, outLen = float_to_hex_string(LenExperiment, LenExperimentInfo)

    print(f'SDAQ2 Sends: {hex_identifier} {outLen} 01')

    message = bytearray.fromhex(hex_identifier + outLen + "01")

    UART.send(message)

    return {"Length of Experiment": actualLen}
