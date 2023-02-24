"""
@author: Nicholas Kwok, Pike Amornchat
Main script for communicating with microcontrollers
hello
"""

import time

from PySerial import UART, list_ports
from server_config import inputInfo
from commands import STBCommand, SDAQCommand, SDAQ2Command, ETB2Command, EDAQCommand, DyeInjectTest

def DAQ_TESTING(port, inputInfo):

    status = {}

    DAQ_UART = UART("DAQ Microcontroller", port) # check this, optionally, specify the port number

    status['SDAQ'] = SDAQCommand(DAQ_UART, 10, inputInfo["Datafreq"]["defaultValue"],
                                 inputInfo["PIVfreq"], inputInfo["Datafreq"])  # TODO replace the second and third arguments with actual values from user input

    time.sleep(0.01)

    status['SDAQ2'] = SDAQ2Command(DAQ_UART, inputInfo["lenExperiment"]['defaultValue'], inputInfo["lenExperiment"])
    
    time.sleep(3) # this should be the time of the experiment 

    status['EDAQ'] = EDAQCommand(DAQ_UART)

    return status

def DyeInjectTestCommand(port, inputInfo):

    status = {}

    TB_UART = UART("TB Microcontroller", port)

    status['Dye Inject Test Command'] = DyeInjectTest(TB_UART)

    return status

def TBTestingCommand(port, inputInfo):

    status = {}

    TB_UART = UART("TB Microcontroller", port)

    status['Dye Inject Test Command'] = DyeInjectTest(TB_UART)

    return status


if __name__ == "__main__":

    '''
    FOR TESTING ONLY -  in the future, a function will be called from this script in server.py

    TODO code functionality to use default values in a "debug" mode

    '''
    
    ports_available = list_ports()

    for port, index in ports_available:
        print(f'SELECTION NUMBER {index}: {port}')

    DAQ_port_index = int(input("Choose DAQ port selection number input should be an integer: "))
    TB_port_index = int(input("Choose TB port selection number input should be an integer: "))

    print(DAQ_TESTING(ports_available[DAQ_port_index], inputInfo))
    print(DyeInjectTestCommand(ports_available[TB_port_index], inputInfo))
    # print(TBTestingCommand(ports_available[TB_port_index], inputInfo))
