import ctypes
import numpy as np
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
from TC08_config import USBTC08_CHANNELS, INPUT_TYPES

USBTC08_MAX_CHANNELS = 8 #Max number of channels TODO: Check final number of Pico Data loggers available

"""
Samples data in an unbroken sequence, for a specified duration in seconds

Outputs CSV file with dictionary of channels with respective temperature values and time stamp. 

"""

def streaming_mode(length):
    # Create chandle and status ready for use
    chandle = ctypes.c_int16()
    status = {}

    # open unit
    status["open_unit"] = tc08.usb_tc08_open_unit()
    assert_pico2000_ok(status["open_unit"])
    chandle = status["open_unit"]

    # set mains rejection to 50 Hz
    status["set_mains"] = tc08.usb_tc08_set_mains(chandle,0)
    assert_pico2000_ok(status["set_mains"])

    # set all channels from TC08_config file

    for channel in USBTC08_CHANNELS:

        input_type = INPUT_TYPES[USBTC08_CHANNELS[channel]['SENSOR_TYPE']]

        status["set_channel"] = tc08.usb_tc08_set_channel(chandle, USBTC08_CHANNELS[channel]['PORT_NO'], input_type)

        assert_pico2000_ok(status["set_channel"])

    # get minimum sampling interval in ms
    status["get_minimum_interval_ms"] = tc08.usb_tc08_get_minimum_interval_ms(chandle)

    assert_pico2000_ok(status["get_minimum_interval_ms"])

    status["run"] = tc08.usb_tc08_run(chandle, status["get_minimum_interval_ms"]) 
    assert_pico2000_ok(status["run"])

    time_interval = status["get_minimum_interval_ms"]/1000

    time.sleep(length)

    number = length/time_interval

    for channel, index in enumerate(USBTC08_CHANNELS):
        
        temp_buffer = (ctypes.c_float * (USBTC08_MAX_CHANNELS) * number)()
        
        times_ms_buffer = (ctypes.c_int32 * number)()
        
        overflow = ctypes.c_int16()
        
        status["get_temp"] = tc08.usb_tc08_get_temp(
            chandle, 
            ctypes.byref(temp_buffer), 
            ctypes.byref(times_ms_buffer),
            number, 
            ctypes.byref(overflow), 
            USBTC08_CHANNELS[channel]['PORT_NO'], 
            0, 
            1
        )

        assert_pico2000_ok(status["get_temp"])

        print("Channel " + channel + " Temperature: " + temp_buffer[index])
    
    # stop unit
    status["stop"] = tc08.usb_tc08_stop(chandle)
    assert_pico2000_ok(status["stop"])

    # close unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])
    print(status)

if __name__ == "__main__":

    streaming_mode(10)