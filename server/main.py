"""
@author: Nicholas Kwok
Main script for communicating with microcontrollers
"""

import ctypes
import numpy as np
import matplotlib.pyplot as plt

from userInputs import userConfig, transientInput, inputInfo

def float_to_binary(x: float, input_range: list, bits: int) -> tuple:

    min_input, max_input = input_range[0], input_range[1]
    
    max_output = 2**bits - 1

    scaled = (x - min_input) / (max_input) * (max_output)

    rounded = round(scaled)
    
    binary = bin(rounded)

    actual = (rounded * max_input) / max_output
    
    return actual, binary

def cleanInputs(dictionary):

    convertedConfig = {}

    for key, value in dictionary.items():

        if value.isdigit():

            convertedConfig[key] = float(value)

        elif value.lower() == "true":

            convertedConfig[key] = True

        elif value.lower() == "false":

            convertedConfig[key] = False

        else:

            convertedConfig[key] = value

    return convertedConfig
