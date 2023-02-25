"""
@author: Nicholas Kwok, Pike Amornchat
List of commands from Central PC side
"""

from Modules import *

from helpers import convert_frequency_to_clock_tick, float_to_hex_string, float_to_base_15, bool_to_hex_string, float_array_to_hex_string, linear_interpolation

def STBCommand(UART, testDelay: float, testDelay_info: dict, start_y: float, start_y_info: dict, branch_temp: float, branch_temp_info: dict, trans_time: float, trans_time_info: dict):

    hex_identifier = "01"

    actualTestDelay, outTestDelay = float_to_hex_string(testDelay, testDelay_info)

    actualStartY, outStartY = float_to_hex_string(start_y, start_y_info)

    actualBranch, outBranch = float_to_hex_string(branch_temp, branch_temp_info)

    actualTransTime, outTransTime = float_to_hex_string(trans_time, trans_time_info)
    
    print(f'STB Sends: {hex_identifier} {outTestDelay} {outStartY} {outBranch} {outTransTime} + 00000000')

    message = bytearray.fromhex(hex_identifier + outTestDelay + outStartY + outBranch + outTransTime + '00000000')

    UART.send(message)

    return {"Testbed Stabilising Delay": actualTestDelay, "Initial Actuator": actualStartY, "Branch Temp": actualBranch, "Transient Exp Time": actualTransTime}

def STB1Command(UART, testDelay: float, syrLen: float, syrLen_Info: dict, syrDia: float, syrDia_Info: dict, vol_inject: float, vol_inject_info: dict, dyeSpeed: float, dyeSpeed_info: dict, enPulse: bool, dutyCycle: float, dutyCycle_info: dict, cyclePeriod: float, cyclePeriod_info: dict):

    # note that testDelay (stabilising time) is not sent over 

    hex_identifier = "OF"

    actualSyrLen, outSyrLen = float_to_hex_string(syrLen, syrLen_Info)

    actualSyrDia, outSyrDia = float_to_hex_string(syrDia, syrDia_Info)

    actual_vol_inject, out_vol_inject = float_to_hex_string(vol_inject, vol_inject_info)

    actualDyeSpeed, outDyeSpeed = float_to_hex_string(dyeSpeed, dyeSpeed_info)

    outEnPulse = bool_to_hex_string(enPulse)

    actualDutyCycle, outDutyCycle = float_to_hex_string(dutyCycle, dutyCycle_info)

    actualCyclePeriod, outCyclePeriod = float_to_hex_string(cyclePeriod, cyclePeriod_info)

    print(f'STB1 Sends: {hex_identifier} {outSyrLen} {outSyrDia} {out_vol_inject} {outDyeSpeed} {outEnPulse} {outDutyCycle} {outCyclePeriod}')

    message = bytearray.fromhex(hex_identifier + outSyrLen + outSyrDia + out_vol_inject + outDyeSpeed + outEnPulse + outDutyCycle + outCyclePeriod)

    UART.send(message)

    # time.sleep(testDelay) this should be a stabilising time

    return {"Syringe Length": actualSyrLen, "Syringe Diameter": actualSyrDia, "Volume Injected": actual_vol_inject, "Dye Speed": actualDyeSpeed, "Enable Pulse": enPulse, "Duty Cycle": actualDutyCycle, "Cycle Period": actualCyclePeriod}

def RTBProcedure(UART, start_y, end_y, nodes, trans_time, preset_config="Linear"):

    # generate actuator_array and time_array based on user input

    if preset_config=="Linear":

        times, y_values = linear_interpolation(start_y, end_y, nodes, trans_time)

    actual_actuator_pos_array = RTBCommand(UART, y_values, times)

    return {"Actuator Position Array": actual_actuator_pos_array, "Time Step": times}


def RTBCommand(UART, actuator_array, times):

    info = {"range": [np.min(actuator_array), np.max(actuator_array)], "bits": 8}

    hex_identifier = "07"

    actual_actuator_pos_array, out_actuator_pos_array = float_array_to_hex_string(actuator_array, info)

    for index in range (1, len(times)):
        message = bytearray.fromhex(hex_identifier + out_actuator_pos_array[index] + "0000000000000000")
        
        UART.send(message)

        time.sleep(times[index] - times[index-1])

    return actual_actuator_pos_array

def ETB1Command(UART):

    message = bytearray.fromhex("09000000000000000000")

    print(f'ETB1 Sends: 09000000000000000000')

    UART.send(message)

    return {"ETB1 Output": message}

def ETB2Command(UART):

    message = bytearray.fromhex("0A000000000000000000")

    print(f'ETB2 Sends: 0A000000000000000000')

    UART.send(message)

    UART.close_port()

    return {"ETB2 Output": message}

def EDAQCommand(UART):

    message = bytearray.fromhex("0B010101")

    print(f'EDAQ Sends: 0B010101')

    UART.send(message)  

    UART.close_port()  # Close UART to DAQ Microcontroller (port 0)

    return {"EDAQ Output": message}

def SDAQCommand(UART: object, PIVfreq_val: float, Datafreq_val: float, PIVfreq_info: dict, Datafreq_info: dict):

    hex_identifier = "03"  # Command specific hex identifier - check documentation for detail

    actualPIV, outPIVticks = convert_frequency_to_clock_tick(PIVfreq_val)

    actualDatafreq, outDatafreq = float_to_base_15(
        Datafreq_val, Datafreq_info)
    
    print(f'SDAQ Sends: {hex_identifier} {outPIVticks} {outDatafreq}')

    message = bytearray.fromhex(hex_identifier + outPIVticks + outDatafreq)

    UART.send(message)

    return {"Logger Frequency": actualDatafreq, "PIV Frequency": actualPIV, "PIV Ticks": outPIVticks}

def SDAQ2Command(UART, LenExperiment, LenExperimentInfo):

    hex_identifier = "0F"

    actualLen, outLen = float_to_base_15(LenExperiment, LenExperimentInfo)

    print(f'SDAQ2 Sends: {hex_identifier} {outLen} 01')

    message = bytearray.fromhex(hex_identifier + outLen + "01")

    UART.send(message)

    return {"Length of Experiment": actualLen}
