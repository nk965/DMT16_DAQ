import ctypes

"""
Hardcoded channel configuration
Check tc08StreamingModeExample line 27 for thermocouple types and int8 equivalent
"""

INPUT_TYPES = {
    "B": ctypes.c_int8(66),
    "E": ctypes.c_int8(69),
    "J": ctypes.c_int8(74),
    "K": ctypes.c_int8(75),
    "N": ctypes.c_int8(78),
    "R": ctypes.c_int8(82),
    "S": ctypes.c_int8(83),
    "T": ctypes.c_int8(84),
    " ": ctypes.c_int8(32),
    "X": ctypes.c_int8(88),
}

USBTC08_CHANNELS = {
    "CHANNEL_1": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 1
    }, 
    "CHANNEL_2": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 2
    }, 
    "CHANNEL_3": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 3
    }, 
    "CHANNEL_4": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 4
    }, 
    "CHANNEL_5": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 5
    }, 
    "CHANNEL_6": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 6
    }, 
    "CHANNEL_7": {
        "SENSOR_TYPE": "K", #TODO: add support for pressure
        "PORT_NO": 7
    }, 
}