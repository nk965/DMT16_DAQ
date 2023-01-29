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

USBTC08_CONFIG = {
    "UNIT_1": {
        "CHANNEL_CJC": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 0,
            "NAME": "Cold Junction Compensation",
            "ENABLE": True
        }, 
        "CHANNEL_1": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 1,
            "NAME": "Depth 4mm",
            "ENABLE": True
        }, 
        "CHANNEL_2": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 2,
            "NAME": "Depth 2mm",
            "ENABLE": True
        }    
    }, 
    "UNIT_2": {
        "CHANNEL_CJC": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 0,
            "NAME": "Cold Junction Compensation",
            "ENABLE": True
        }, 
        "CHANNEL_1": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 1,
            "NAME": "Depth 4mm",
            "ENABLE": True
        }, 
        "CHANNEL_2": {
            "SENSOR_TYPE": "K",
            "CHANNEL_NO": 2,
            "NAME": "Depth 4mm",
            "ENABLE": True
        }    
    }
}

EXPERIMENT_CONFIG = {
    "recording_period": 10,
    "polling_interval": 3,
    "sampling_interval_ms": 1000
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
}

