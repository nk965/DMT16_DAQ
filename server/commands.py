"""
@author: Nicholas Kwok, Pike Amornchat
List of commands from Central PC side
"""

from Modules import *

from helpers import convert_frequency_to_clock_tick, float_to_hex_string, float_to_base_15, bool_to_pulse_string, float_array_to_hex_string, linear_interpolation, int_to_hex_string

def ITBCommand(UART, testDelay:float, testDelay_info: dict):

    hex_identifier = "14"

    actualTestDelay, outTestDelay = float_to_hex_string(testDelay, testDelay_info)

    message = bytearray.fromhex(hex_identifier + outTestDelay + '0000')

    print(f'ITB Sends: {hex_identifier} {outTestDelay} 0000 in the form of {message}')

    UART.send(message)

    # time.sleep(testDelay) this should be a stabilising time

    return {"Testbed Stabilising Delay": actualTestDelay}


def STBCommand(UART, start_y: float, start_y_info: dict, trans_time: float, trans_time_info: dict):

    hex_identifier = "01"

    actualStartY, outStartY = float_to_hex_string(start_y, start_y_info)

    actualTransTime, outTransTime = float_to_hex_string(trans_time, trans_time_info)

    message = bytearray.fromhex(hex_identifier + outStartY + outTransTime)

    print(f'STB Sends: {hex_identifier} {outStartY} {outTransTime} in the form of {message}')

    UART.send(message)

    return {"Initial Actuator": actualStartY, "Transient Exp Time": actualTransTime}

def STB2Command(UART, branch_temp: float, branch_temp_info: dict):

    hex_identifier = "11"

    actualBranch, outBranch = float_to_hex_string(branch_temp, branch_temp_info)

    message = bytearray.fromhex(hex_identifier + outBranch + '00')

    print(f'STB2 Sends: {hex_identifier} {outBranch}  00 in the form of {message}')

    UART.send(message)

    return {"Branch Temp": actualBranch}


def IDYECommand(UART, syrDia: float, vol_inject: float, inject_time: float, dutyCycle: float, dutyCycle_info: dict, enPulse: bool):

    hex_identifier = "15"

    steps_per_rev = 200

    mm_per_rev = 0.5

    if enPulse: 

        actualDutyCycle, outDutyCycle = float_to_hex_string(dutyCycle, dutyCycle_info)

        steps_per_second = math.floor((steps_per_rev * mm_per_rev * 4 * vol_inject * 1000)/(math.pi * inject_time * actualDutyCycle * syrDia**2)) # this should be an integer between 1 and 65536 TODO add error checking for this 

    else:

        steps_per_second = math.floor((steps_per_rev * mm_per_rev * 4 * vol_inject * 1000)/(math.pi * inject_time * syrDia**2)) # this should be an integer between 1 and 65536 TODO add error checking for this 

    outspeed = int_to_hex_string(steps_per_second, 16) # steps per second is 100

    message = bytearray.fromhex(hex_identifier + outspeed + '00')

    print(f'IDYE Sends: {hex_identifier} {outspeed} 00 in the form of: {message}')

    UART.send(message)

    return {"Steps Per Second (Speed)": steps_per_second}

def IDYE2Command(UART, dutyCycle: float, dutyCycle_info: dict, cyclePeriod: float, cyclePeriod_info: dict):

    hex_identifier = "13"

    actualDutyCycle, outDutyCycle = float_to_hex_string(dutyCycle, dutyCycle_info) # TODO HARD CODE THIS 

    outCyclePeriod = int_to_hex_string(cyclePeriod*100, cyclePeriod_info['bits']) # encode cyclePeriod to 0.01 precision second intervals, TODO add error checking? Max cyclePeriod is 655.35

    message = bytearray.fromhex(hex_identifier + outDutyCycle + outCyclePeriod)

    print(f'IDYE2 Sends: {hex_identifier} {outDutyCycle} {outCyclePeriod} in the form of: {message}')

    UART.send(message)

    return {"Duty Cycle": actualDutyCycle, "Cycle Period": outCyclePeriod}

def IDYE3Command(UART, enPulse: bool, syrDia: float, vol_inject: float):

    hex_identifier = "18"

    steps_per_rev = 200

    mm_per_rev = 0.5

    steps = math.floor((steps_per_rev * mm_per_rev * 4 * vol_inject * 1000)/(math.pi * syrDia**2)) # this should be an integer between 1 and 65536 TODO add error checking for this 

    outEnPulse = bool_to_pulse_string(enPulse)

    if enPulse: 

        outSteps = int_to_hex_string(steps,16)


    outSteps = int_to_hex_string(steps, 16) # TODO UNHARD CODE THIS 

    message = bytearray.fromhex(hex_identifier + outEnPulse + outSteps) 

    print(f'IDYE3 Sends: {hex_identifier} {outEnPulse} {outSteps} in the form of: {message}')

    UART.send(message)

    return {"Steps": steps, "Pulse Mode": enPulse}


def RTBProcedure(UART, start_y, end_y, nodes, trans_time, preset_config="Linear"):

    # generate actuator_array and time_array based on user input

    if preset_config=="Linear":

        times, y_values = linear_interpolation(start_y, end_y, nodes, trans_time)

    actual_actuator_pos_array = RTBCommand(UART, y_values, times)

    return {"Actuator Position Array": actual_actuator_pos_array, "Time Step": times}


def TestCommand(UART):

    hex_identifier = '69'

    message = bytearray.fromhex(hex_identifier + "010101")

    print(f'TestCommand Sends: {hex_identifier} + 010101 in the form of {message}')

    UART.send(message)

    return {}

def RTBCommand(UART, actuator_array, times):

    info = {"range": [np.min(actuator_array), np.max(actuator_array)], "bits": 16}

    hex_identifier = "07"

    actual_actuator_pos_array, out_actuator_pos_array = float_array_to_hex_string(actuator_array, info)

    for index in range(1, len(times)):

        # toggle padding

        if index % 2 == 0:
            padding = "01"

        else:
            padding = "00"

        message = bytearray.fromhex(hex_identifier + out_actuator_pos_array[index] + padding)
        
        print(f'RTB Sends: {hex_identifier} {out_actuator_pos_array[index]} {padding} in the form of {message}')
        UART.send(message)

        time.sleep(times[index] - times[index-1])

    return actuator_array

def ETB1Command(UART):

    message = bytearray.fromhex("09000000")

    print(f'ETB1 Sends: 09000000 in the form of {message}')

    UART.send(message)

    return {"ETB1 Output": message}

def ETB2Command(UART):

    message = bytearray.fromhex("0A000000")

    print(f'ETB2 Sends: 0A000000 in the form of {message}')

    UART.send(message)

    UART.close_port()

    return {"ETB2 Output": message}

def EDAQCommand(UART):

    message = bytearray.fromhex("0B010101")

    print(f'EDAQ Sends: 0B010101 in the form of {message}')

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

    actualLen, outLen = float_to_base_15(LenExperiment+30, LenExperimentInfo)

    print(f'SDAQ2 Sends: {hex_identifier} {outLen} 01')

    message = bytearray.fromhex(hex_identifier + outLen + "01")

    UART.send(message)

    return {"Length of Experiment": actualLen}
