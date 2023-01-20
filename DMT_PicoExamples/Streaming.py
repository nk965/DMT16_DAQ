import ctypes
import numpy as np
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
from TC08_config import USBTC08_CHANNELS_STREAMING, INPUT_TYPES

USBTC08_MAX_CHANNELS = 8 #Max number of channels TODO: Check final number of Pico Data loggers available

def record_data(recording_period):

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

    # set CJC channel 

    status["set_channel"] = tc08.usb_tc08_set_channel(chandle, 0, INPUT_TYPES["K"])
    assert_pico2000_ok(status["set_channel"])

    # set all channels from TC08_config file

    for channel in USBTC08_CHANNELS_STREAMING:

        input_type = INPUT_TYPES[USBTC08_CHANNELS_STREAMING[channel]['SENSOR_TYPE']]

        status["set_channel"] = tc08.usb_tc08_set_channel(chandle, USBTC08_CHANNELS_STREAMING[channel]['CHANNEL_NO'], input_type)
        assert_pico2000_ok(status["set_channel"])

    # obtain minimum interval between sample 
    
    status["get_minimum_interval_ms"] = tc08.usb_tc08_get_minimum_interval_ms(chandle)
    assert_pico2000_ok(status["get_minimum_interval_ms"])

    # run data logger at fastest possible sample frequency

    status["run"] = tc08.usb_tc08_run(chandle, status["get_minimum_interval_ms"]) 
    assert_pico2000_ok(status["run"])

    # run data logger at specified period
    
    time.sleep(recording_period)

    BUFFER_SIZE = 64

    temp_info = {}

    for index, (channel, info) in enumerate(USBTC08_CHANNELS_STREAMING.items()):

        print(f"Iteration: {index}")

        temp_buffer = (ctypes.c_float * (int(BUFFER_SIZE)))()
        
        times_ms_buffer = (ctypes.c_int32 * int(BUFFER_SIZE))()
        
        overflow = ctypes.c_int16()

        temp_info[channel] = {}

        status["get_temp"] = tc08.usb_tc08_get_temp_deskew(
            chandle, 
            ctypes.byref(temp_buffer), 
            ctypes.byref(times_ms_buffer),
            ctypes.c_int32(BUFFER_SIZE), 
            ctypes.byref(overflow), 
            info['CHANNEL_NO'], 
            0, 
            0
        )

        print(tc08.usb_tc08_get_last_error(chandle))
        assert_pico2000_ok(status["get_temp"])

        temp_info[channel]["Temperatures"] = np.asarray(temp_buffer)
        temp_info[channel]["Time Intervals"] = np.asarray(times_ms_buffer)
        temp_info[channel]["Overflow"] = overflow

    print(temp_info)

    # stop unit
    status["stop"] = tc08.usb_tc08_stop(chandle)
    assert_pico2000_ok(status["stop"])

    # close unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])
    print(status)

    return status

if __name__ == "__main__":

    # set length recording in seconds

    recording_period = 5

    record_data(recording_period)

