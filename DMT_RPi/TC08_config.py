import ctypes

"""
@author: Nicholas Kwok
Hardcoded channel configuration, TODO: this configuration should be determined by the JavaScript/Python UI
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

# default configuration 

USBTC08_CONFIG = {
    "UNIT1": {
        "CHANNELCJC": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 0,
            "NAME": "Cold Junction Compensation",
            "ENABLE": True
        }, 
        "CHANNEL1": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 1,
            "NAME": "Depth 4mm",
            "ENABLE": True
        }, 
        "CHANNEL2": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 2,
            "NAME": "Depth 3mm",
            "ENABLE": True
        },
        "CHANNEL3": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 3,
            "NAME": "Depth 2mm",
            "ENABLE": True
        }, 
        "CHANNEL4": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 4,
            "NAME": "Depth 1mm",
            "ENABLE": True
        },
        "CHANNEL5": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 5,
            "NAME": "Depth 4mm",
            "ENABLE": True
        }, 
        "CHANNEL6": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 6,
            "NAME": "Depth 3mm",
            "ENABLE": True
        },
        "CHANNEL7": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 7,
            "NAME": "Depth 2mm",
            "ENABLE": True
        },
        "CHANNEL8": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 8,
            "NAME": "Depth 1mm",
            "ENABLE": True
        }         
    }, 
    "UNIT2": {
        "CHANNELCJC": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 0,
            "NAME": "Cold Junction Compensation",
            "ENABLE": True
        }, 
        "CHANNEL1": {
            "SENSOR_TYPE": "X",
            "CHANNEL_NO": 1,
            "NAME": "Depth 4mm",
            "ENABLE": True
        }, 
        "CHANNEL2": {
            "SENSOR_TYPE": "X",
            "CHANNEL_NO": 2,
            "NAME": "Depth 3mm",
            "ENABLE": True
        },
        "CHANNEL3": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 3,
            "NAME": "Depth 2mm",
            "ENABLE": True
        }, 
        "CHANNEL4": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 4,
            "NAME": "Depth 1mm",
            "ENABLE": True
        },
        "CHANNEL5": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 5,
            "NAME": "Depth 4mm",
            "ENABLE": True
        }, 
        "CHANNEL6": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 6,
            "NAME": "Depth 3mm",
            "ENABLE": True
        },
        "CHANNEL7": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 7,
            "NAME": "Depth 2mm",
            "ENABLE": True
        },
        "CHANNEL8": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 8,
            "NAME": "Depth 1mm",
            "ENABLE": True
        }    
    }
}

EXPERIMENT_CONFIG = {
    "recording_period": 10,
    "polling_interval": 3,
    "sampling_interval_ms": 100
}

