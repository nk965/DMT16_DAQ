"""
@author: Nicholas Kwok, Pike Amornchat
Main script for communicating with microcontrollers
hello
"""

from Modules import *

from PySerial import UART, list_ports
from server_config import inputInfo
from commands import STBCommand, SDAQCommand, SDAQ2Command, ETB1Command, ETB2Command, EDAQCommand, RTBProcedure, ITBCommand, STB2Command, IDYECommand, IDYE2Command, IDYE3Command

def DAQ_TESTING(port: str, inputInfo):
    '''
    Benchscale Test
    '''

    logs = {}

    DAQ_UART = UART("DAQ Microcontroller", port) # check this, optionally, specify the port number

    logs['SDAQ'] = SDAQCommand(DAQ_UART, inputInfo['PIVfreq']['defaultValue'], inputInfo["Datafreq"]["defaultValue"],
                                 inputInfo["PIVfreq"], inputInfo["Datafreq"])  # TODO replace the second and third arguments with actual values from user input

    time.sleep(1)
    
    logs['SDAQ2'] = SDAQ2Command(DAQ_UART, inputInfo["lenExperiment"]['defaultValue'], inputInfo["lenExperiment"])

    time.sleep(inputInfo['lenExperiment']['defaultValue'])

    logs['EDAQ'] = EDAQCommand(DAQ_UART)

    return logs

def TB_TESTING(port: str, inputInfo):
    '''
    Benchscale Test
    '''

    logs = {}

    TB_UART = UART("TB Microcontroller", port)

    logs['ITB'] = ITBCommand(TB_UART, inputInfo["stabilising_delay"]['defaultValue'], inputInfo['stabilising_delay']) # TODO ask Pike if this is necessary 

    logs['STB'] = STBCommand(TB_UART, inputInfo["start_y"]["defaultValue"], inputInfo["start_y"], inputInfo["trans_time"]["defaultValue"], inputInfo["trans_time"])

    logs['STB2'] = STB2Command(TB_UART, inputInfo['branch_temp']['defaultValue'], inputInfo['branch_temp'])

    logs['IDYE'] = IDYECommand(TB_UART, inputInfo['syrDia']['defaultValue'], inputInfo['vol_inject']['defaultValue'], inputInfo['inject_time']['defaultValue'], inputInfo['dutyCycle']['defaultValue'], inputInfo['dutyCycle'], inputInfo['enPulse'])

    logs['IDYE2'] = IDYE2Command(TB_UART, inputInfo['dutyCycle']['defaultValue'], inputInfo['dutyCycle'], inputInfo['cyclePeriod']['defaultValue'], inputInfo['cyclePeriod'])

    logs['IDYE3'] = IDYE3Command(TB_UART, inputInfo['enPulse']['defaultValue'], inputInfo['syrDia']['defaultValue'], inputInfo['vol_inject']['defaultValue'])

    time.sleep(0.5*(inputInfo['inject_time']['defaultValue'] - inputInfo['trans_time']['defaultValue']))

    time.sleep(inputInfo['inject_time']['defaultValue']) # TEMPORARY

    logs['RTB'] = RTBProcedure(TB_UART, inputInfo["start_y"]["defaultValue"], inputInfo["end_y"]["defaultValue"], inputInfo["nodes"]["defaultValue"], inputInfo["trans_time"]["defaultValue"], inputInfo["presetConfig"]["defaultValue"])  

    logs['ETB1'] = ETB1Command(TB_UART) 

    time.sleep(0.5*(inputInfo['inject_time']['defaultValue'] - inputInfo['trans_time']['defaultValue']))

    logs['ETB2'] = ETB2Command(TB_UART)

    return logs

def process(DAQ_port: str, TB_port: str, inputs, info): 

    logs = {}

    TB_UART = UART("TB Microcontroller", TB_port)
    DAQ_UART = UART("DAQ Microcontroller", DAQ_port)

    logs['ITB'] = ITBCommand(TB_UART, inputs["stabilising_delay"], info['stabilising_delay']) 

    logs['STB'] = STBCommand(TB_UART, inputs["start_y"], info["start_y"], inputs["trans_time"], info["trans_time"])

    logs['STB2'] = STB2Command(TB_UART, inputs['branch_temp'], info['branch_temp'])

    logs['IDYE'] = IDYECommand(TB_UART, inputs['syrDia'], inputs['vol_inject'], inputs['inject_time'], inputs['dutyCycle'], info['dutyCycle'], inputs['enPulse'])

    logs['IDYE2'] = IDYE2Command(TB_UART, inputs['dutyCycle'], info['dutyCycle'], inputs['cyclePeriod'], info['cyclePeriod'])

    time.sleep(inputs["stabilising_delay"])

    logs['SDAQ'] = SDAQCommand(DAQ_UART, inputs["PIVfreq"], inputs["Datafreq"], info["PIVfreq"], info["Datafreq"]) 

    time.sleep(1)

    logs['SDAQ2'] = SDAQ2Command(DAQ_UART, inputs["lenExperiment"], info["lenExperiment"]) 

    time.sleep(15)

    time.sleep(0.5*(inputs['lenExperiment'] - inputs['inject_time']))

    logs['IDYE3'] = IDYE3Command(TB_UART, inputs['enPulse'], inputs['syrDia'], inputs['vol_inject'])

    time.sleep(0.5*(inputs['inject_time'] - inputs['trans_time']))
    
    logs['RTB'] = RTBProcedure(TB_UART, inputs["start_y"], inputs["end_y"], inputs["nodes"], inputs["trans_time"], inputs["presetConfig"])

    logs['ETB1'] = ETB1Command(TB_UART) 
    
    time.sleep(0.5*(inputs['inject_time'] - inputs['trans_time']))  

    logs['ETB2'] = ETB2Command(TB_UART)

    time.sleep(0.5*(inputs['lenExperiment'] - inputs['inject_time']))

    logs['EDAQ'] = EDAQCommand(DAQ_UART)

    return logs

def run(DAQ_port: str, TB_port: str, inputs=None):

    if inputs is None:
        inputs = {key: inputInfo[key]["defaultValue"] for key in inputInfo}

    system_logs = process(DAQ_port, TB_port, inputs, inputInfo)

    return system_logs

if __name__ == "__main__":

    '''
    FOR DEBUGGING - USE JAVASCRIPT GUI 
    '''

    ports_available = list_ports()

    for port, index in enumerate(ports_available):
        print(f'SELECTION {port}: {index}')

    DAQ_port_index = int(input("Choose DAQ port selection number (input should be an integer): "))
    TB_port_index = int(input("Choose TB port selection number (input should be an integer): "))

    # logs = TB_TESTING(ports_available[TB_port_index], inputInfo) # Benchscale Test for TB system
    # logs = DAQ_TESTING(ports_available[DAQ_port_index], inputInfo) # Benchscale Test for DAQ system

    logs = run(ports_available[DAQ_port_index], ports_available[TB_port_index])

    print(logs)

