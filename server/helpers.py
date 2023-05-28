"""
@author: Nicholas Kwok, Pike Amornchat
Helper functions for command protocols
"""

from Modules import *

def linear_interpolation(start_y: float, end_y: float, nodes: int, time: float) -> tuple:
    """
    Returns an array of times (with the correct number of nodes) and an array of y assuming linear interpolation
    
    Args:
    start_y: float, starting value of y
    end_y: float, ending value of y
    nodes: int, number of nodes for interpolation
    time: float, total time
    
    Returns:
    tuple, consisting of two numpy arrays: (1) array of times and (2) array of y values
    """
    # Calculate time step between each node
    time_step = time / (nodes - 1)
    
    # Create array of times
    times = np.arange(0, time + time_step, time_step)[:nodes]
    
    # Calculate slope between start_y and end_y
    slope = (end_y - start_y) / (nodes - 1)
    
    # Calculate array of y values using linear interpolation
    y_values = start_y + slope * np.arange(nodes)
    
    return times, y_values

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
        "10": "a",
        "11": "b",
        "12": "c",
        "13": "d",
        "14": "e",
        "15": "f"
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

def int_to_hex_string(n: int, bits: int) -> str:

    capped_no = max(0, min((16**(bits // 4) - 1), round(n)))

    hex_string = hex(capped_no)[2:].zfill(bits // 4)

    return hex_string

def float_to_hex_string(value: float, info: dict) -> tuple: #TODO not maximising resolution for Arduino Serial

    min_input, max_input = info["range"][0], info["range"][1]

    max_output = 16**(info["bits"] // 4) - 1

    min_output = 0

    scaled = (((value - min_input) / (max_input - min_input))
              * (max_output - min_output)) + min_output

    rounded = round(scaled)

    actual = (((rounded - min_output) * (max_input - min_input)) /
              (max_output - min_output)) + min_input

    hex_string = int_to_hex_string(rounded, info["bits"])

    return actual, hex_string

def bool_to_pulse_string(value: bool): 

    if value == True:

        hex_string = "70" # ASCII representation of 'p' in hex (enables pulse mode)
        
    else:

        hex_string = "74" # ASCII representation of 't' in hex (disables pulse mode)

    return hex_string

def float_to_base_15(value: float, info:dict) -> tuple:

    min_input, max_input = info["range"][0], info["range"][1]

    max_output = 15**(info["bits"] // 4) - 1

    min_output = 0

    scaled = (((value - min_input) / (max_input - min_input))
              * (max_output - min_output)) + min_output

    rounded = round(scaled)

    actual = (((rounded - min_output) * (max_input - min_input)) /
              (max_output - min_output)) + min_input

    return actual, base_15_protocol_convert(rounded) 

def float_array_to_hex_string(arr: np.ndarray, info: dict) -> np.ndarray:

    scaled_arr = ((arr - info["range"][0]) / (info["range"][1] - info["range"][0])) * (65.535 - 0) + 0 

    rounded = np.round(scaled_arr*1000).astype(int)

    hex_func = np.vectorize(lambda x: int_to_hex_string(x, info["bits"]))

    hex_string_array = hex_func(rounded)

    print(hex_string_array)

    return rounded, hex_string_array

def cleanInputs(dictionary):
    convertedConfig = {}

    for key, value in dictionary.items():
        if isinstance(value, int):
            convertedConfig[key] = value
        elif isinstance(value, float):
            convertedConfig[key] = value
        elif value.isdigit():
            convertedConfig[key] = int(value)
        elif value.lower() == "true":
            convertedConfig[key] = True
        elif value.lower() == "false":
            convertedConfig[key] = False
        else:
            try:
                convertedConfig[key] = float(value)
            except ValueError:
                convertedConfig[key] = value

    return convertedConfig