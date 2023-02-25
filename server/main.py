"""
@author: Nicholas Kwok, Pike Amornchat
Main script for communicating with microcontrollers
hello
"""

from Modules import *

from PySerial import UART, list_ports
from server_config import inputInfo
from commands import STBCommand, STB1Command, SDAQCommand, SDAQ2Command, ETB1Command, ETB2Command, EDAQCommand, STB1Command, RTBProcedure

def DAQ_TESTING(port, inputInfo):

    status = {}

    DAQ_UART = UART("DAQ Microcontroller", port) # check this, optionally, specify the port number

    status['SDAQ'] = SDAQCommand(DAQ_UART, 10, inputInfo["Datafreq"]["defaultValue"],
                                 inputInfo["PIVfreq"], inputInfo["Datafreq"])  # TODO replace the second and third arguments with actual values from user input

    time.sleep(0.01) 

    status['SDAQ2'] = SDAQ2Command(DAQ_UART, inputInfo["lenExperiment"]['defaultValue'], inputInfo["lenExperiment"])
    
    time.sleep(5) # this should be how long the Pico Logger is Logging for i.e., lenExperiment

    status['EDAQ'] = EDAQCommand(DAQ_UART)

    return status

def TB_TESTING(port, inputInfo):

    status = {}

    TB_UART = UART("TB Microcontroller", port)

    status['STB'] = STBCommand(TB_UART, inputInfo["stabilising_delay"]["defaultValue"], inputInfo["stabilising_delay"], inputInfo["start_y"]["defaultValue"], inputInfo["start_y"], inputInfo["branch_temp"]["defaultValue"], inputInfo["branch_temp"], inputInfo["trans_time"]["defaultValue"], inputInfo["trans_time"])

    time.sleep(3)

    status['STB1'] = STB1Command(TB_UART, inputInfo["stabilising_delay"]["defaultValue"], inputInfo["syrLen"]["defaultValue"], inputInfo["syrLen"], inputInfo["syrDia"]["defaultValue"], inputInfo["syrDia"], inputInfo["vol_inject"]["defaultValue"], inputInfo["vol_inject"], inputInfo["dyeSpeed"]["defaultValue"], inputInfo["dyeSpeed"], inputInfo["enPulse"]["defaultValue"], inputInfo["dutyCycle"]["defaultValue"], inputInfo["dutyCycle"], inputInfo["cyclePeriod"]["defaultValue"], inputInfo["cyclePeriod"])

    time.sleep(3)

    actuator_array = np.array([])
    time_array = np.array([])

    status['RTB'] = RTBProcedure(TB_UART, actuator_array, time_array) # TODO 

    time.sleep(3)
    
    status['ETB1'] = ETB1Command(TB_UART) 
    
    time.sleep(3)

    status['ETB2'] = ETB2Command(TB_UART)

    return status

def process(DAQ_port, TB_port, inputs, info): 

    status = {}

    TB_UART = UART("TB Microcontroller", port)
    DAQ_UART = UART("DAQ Microcontroller", port)

    status['STB'] = STBCommand(TB_UART, inputs["stabilising_delay"], info["stabilising_delay"], inputs["start_y"], info["start_y"], inputs["branch_temp"], info["branch_temp"], inputs["trans_time"], info["trans_time"])

    # time.sleep(3) wait for Serial communication to finish (test if needed)

    status['STB1'] = STB1Command(TB_UART, inputs["stabilising_delay"], inputs["syrLen"], info["syrLen"], inputs["syrDia"], info["syrDia"], inputs["vol_inject"], info["vol_inject"], inputs["dyeSpeed"], info["dyeSpeed"], inputs["enPulse"], inputs["dutyCycle"], info["dutyCycle"], inputs["cyclePeriod"], info["cyclePeriod"])

    time.sleep(inputs["stabilising_delay"]) # Stabilising delay, tune to how long testbed needs and dye injection needs

    status['SDAQ'] = SDAQCommand(DAQ_UART, inputs["PIVfreq"], inputs["Datafreq"], info["PIVfreq"], info["Datafreq"]) 

    # lenExperiment for Pico Data logger (i.e., time between SDAQ, EDAQ), note that lenExperiment must GREATER than trans_time. 

    status['SDAQ2'] = SDAQ2Command(DAQ_UART, inputs["lenExperiment"], info["lenExperiment"]) 
    
    status['RTB'] = RTBProcedure(TB_UART, inputs['start_y'], inputs['end_y'], inputs['nodes'], inputs['trans_time'], inputs['preset_config'])

    time.sleep(inputs["trans_time"])

    status['ETB1'] = ETB1Command(TB_UART)

    status['ETB2'] = ETB2Command(TB_UART)

    time.sleep(inputs["lenExperiment"] - inputs["trans_time"]) 

    status['EDAQ'] = EDAQCommand(DAQ_UART)

    return status

def run(inputs=None):

    if inputs is None:
        inputs = {key: inputInfo[key]["defaultValue"] for key in inputInfo}

    ports_available = list_ports()

    for port, index in enumerate(ports_available):
        print(f'SELECTION {index}: {port}')

    DAQ_port_index = int(input("Choose DAQ port selection number input should be an integer: "))
    TB_port_index = int(input("Choose TB port selection number input should be an integer: "))

    return process(ports_available[DAQ_port_index], ports_available[TB_port_index], inputs, inputInfo)

if __name__ == "__main__":

    '''
    FOR TESTING ONLY -  in the future, a process() will be called from this script in server.py

    TODO code functionality to use default values in a "debug" mode

    '''
    
    ports_available = list_ports()

    for port, index in enumerate(ports_available):
        print(f'SELECTION {index}: {port}')

    DAQ_port_index = int(input("Choose DAQ port selection number input should be an integer: "))
    TB_port_index = int(input("Choose TB port selection number input should be an integer: "))

    # print(DAQ_TESTING(ports_available[DAQ_port_index], inputInfo))
    print(TB_TESTING(ports_available[TB_port_index], inputInfo))

