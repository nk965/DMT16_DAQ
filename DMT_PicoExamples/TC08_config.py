import ctypes

"""
Hardcoded channel configuration
Check tc08StreamingModeExample line 27 for thermocouple types and int8 equivalent
"""

INPUT_TYPES = {
    "B": ctypes.c_int8(66),
    "E": ctypes.c_int8(69),
    "J": ctypes.c_int8(74),
    "K": ctypes.c_int8(75), # type K thermocouples
    "N": ctypes.c_int8(78),
    "R": ctypes.c_int8(82),
    "S": ctypes.c_int8(83),
    "T": ctypes.c_int8(84),
    " ": ctypes.c_int8(32),
    "X": ctypes.c_int8(88), # mV readings 
}

USBTC08_CHANNELS = {
    "CHANNEL_CJC": {
        "SENSOR_TYPE": " ",
        "PORT_NO": 0,
        "NAME": "Cold Junction Compensation",
    }, 
    "CHANNEL_1": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 1,
        "NAME": "Depth 4mm",
    }, 
    "CHANNEL_2": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 2,
        "NAME": "Depth 2mm",
    }, 
    "CHANNEL_3": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 3,
        "NAME": "Depth 1mm",
    }, 
}

USBTC08_CHANNELS_2 = {
    "CHANNEL_1": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 1,
        "NAME": "NAME_X"
    }, 
    "CHANNEL_2": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 2,
        "NAME": "NAME_X"
    }, 
    "CHANNEL_3": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 3,
        "NAME": "NAME_X"
    }, 
    "CHANNEL_4": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 4,
        "NAME": "NAME_X"
    }, 
    "CHANNEL_5": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 5,
        "NAME": "NAME_X"
    }, 
    "CHANNEL_6": {
        "SENSOR_TYPE": "K",
        "PORT_NO": 6,
        "NAME": "NAME_X"
    }, 
    "CHANNEL_7": {
        "SENSOR_TYPE": "K", #TODO: add support for pressure
        "PORT_NO": 7,
        "NAME": "NAME_X"
    },
    "CHANNEL_8": {
        "SENSOR_TYPE": "K", #TODO: add support for pressure
        "PORT_NO": 8,
        "NAME": "NAME_X"
    },
}