"""
@author: Nicholas Kwok, Pike Amornchat
Helper functions for command protocols
"""

from Modules import *

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

    return actual, rounded

def bool_to_hex_string(value: bool): 

    if value == True:

        hex_string = "0001"

    else:

        hex_string = "0000"

    return hex_string

def float_to_base_15(value: float, info:dict) -> tuple:

    actual, rounded = float_to_hex_string(value, info)

    return actual, base_15_protocol_convert(rounded) 
