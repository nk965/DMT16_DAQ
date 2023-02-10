"""
@author: Nicholas Kwok
Main script for communicating with microcontrollers
"""

import ctypes
import math
import numpy as np
import matplotlib.pyplot as plt

from userInputs import userConfig, transientInput

convertedConfig = {}

for key, value in userConfig.items():
    if value.isdigit():
        convertedConfig[key] = int(value)
    elif value.lower() == "true":
        convertedConfig[key] = True
    elif value.lower() == "false":
        convertedConfig[key] = False
    else:
        convertedConfig[key] = value

#f is frequency input

f = np.arange(10,20000,1) # in Hz

no_ticks = np.round(84*10**6/(129*f),1) #TODO: send this in binary through serial port

#TODO: UTF-8 characters 

#binary bin(30) e.g. 

f_actual = 84*10**6/(129*no_ticks)

# plt.scatter(f,f)
# print(f_actual)
plt.scatter(f,f_actual-f)
plt.show()




