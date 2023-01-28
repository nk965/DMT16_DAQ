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

USBCTC08_CONFIG = {
    "UNIT 1": {
        "CHANNEL_CJC": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 0,
            "NAME": "Cold Junction Compensation",
        }, 
        "CHANNEL_1": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 1,
            "NAME": "Depth 4mm",
        }, 
        "CHANNEL_2": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 2,
            "NAME": "Depth 2mm",
        }    
    }, 
    "UNIT 2": {
        "CHANNEL_CJC": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 0,
            "NAME": "Cold Junction Compensation",
        }, 
        "CHANNEL_1": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 1,
            "NAME": "Depth 4mm",
        }, 
        "CHANNEL_2": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 2,
            "NAME": "Depth 4mm",
        }    
    }
}

USBTC08_CHANNELS = {
    "CHANNEL_CJC": {
        "SENSOR_TYPE": "K",
        "CHANNEL_NO": 0,
        "NAME": "Cold Junction Compensation",
    }, 
    "CHANNEL_1": {
        "SENSOR_TYPE": "K",
        "CHANNEL_NO": 1,
        "NAME": "Depth 4mm",
    }, 
    "CHANNEL_2": {
        "SENSOR_TYPE": "K",
        "CHANNEL_NO": 2,
        "NAME": "Depth 4mm",
    },
    "CHANNEL_3": {
        "SENSOR_TYPE": "K",
        "CHANNEL_NO": 3,
        "NAME": "Depth 4mm",
    }, 
    "CHANNEL_4": {
        "SENSOR_TYPE": "K",
        "CHANNEL_NO": 4,
        "NAME": "Depth 4mm",
    }, 
    "CHANNEL_5": {
        "SENSOR_TYPE": "K",
        "CHANNEL_NO": 5,
        "NAME": "Depth 4mm",
    }, 
    "CHANNEL_6": {
        "SENSOR_TYPE": "K",
        "CHANNEL_NO": 6,
        "NAME": "Depth 4mm",
    }, 
    "CHANNEL_7": {
        "SENSOR_TYPE": "K",
        "CHANNEL_NO": 7,
        "NAME": "Depth 4mm",
    }, 
    "CHANNEL_8": {
        "SENSOR_TYPE": "K",
        "CHANNEL_NO": 8,
        "NAME": "Depth 4mm",
    }, 
}

