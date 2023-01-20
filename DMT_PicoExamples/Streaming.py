import ctypes
import numpy as np
import time
import math
import pandas as pd
from datetime import datetime, timedelta
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
from TC08_config import USBTC08_CHANNELS, INPUT_TYPES

"""
Samples data in an unbroken sequence, for a specified duration in seconds

Outputs CSV file with dictionary of channels with respective temperature values and time stamp. 

"""


def record_data(recording_period, sampling_interval_ms):

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

    for channel in USBTC08_CHANNELS:

        input_type = INPUT_TYPES[USBTC08_CHANNELS[channel]['SENSOR_TYPE']]

        status["set_channel"] = tc08.usb_tc08_set_channel(chandle, USBTC08_CHANNELS[channel]['CHANNEL_NO'], input_type)
        assert_pico2000_ok(status["set_channel"])

    # run data logger at fastest possible sample frequency or specified frequency 
    
    status["interval_ms"] = sampling_interval_ms if sampling_interval_ms >= tc08.usb_tc08_get_minimum_interval_ms(chandle) else tc08.usb_tc08_get_minimum_interval_ms(chandle)
    assert_pico2000_ok(status["interval_ms"])

    status["run"] = tc08.usb_tc08_run(chandle, status["interval_ms"]) 
    assert_pico2000_ok(status["run"])

    # run data logger for specified period
    
    time.sleep(recording_period)
    start_time = datetime.now()

    BUFFER_SIZE = math.ceil(recording_period / (status["run"] / 1000)) 

    temp_info = {}

    for index, (channel, info) in enumerate(USBTC08_CHANNELS.items()):

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

        assert_pico2000_ok(status["get_temp"])

        temp_info[channel]["Temperatures"] = np.asarray(temp_buffer)
        temp_info[channel]["Time Intervals"] = np.asarray(times_ms_buffer)
        temp_info[channel]["Overflow"] = overflow

    # stop unit
    status["stop"] = tc08.usb_tc08_stop(chandle)
    assert_pico2000_ok(status["stop"])

    # close unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])
    print(status)

    # post processing: adding time stamps

    for channel in temp_info:

        start_timestamp = int(start_time.timestamp() * 1000)

        # add the intervals (in milliseconds) to the start timestamp
        timestamps_ms = start_timestamp + temp_info[channel]["Time Intervals"]

        # convert the timestamps in ms to datetime
        timestamps = [datetime.fromtimestamp(ts/1000) for ts in timestamps_ms]

        # format the timestamp
        formatted_timestamps = [timestamp.strftime("%M:%S:%f") for timestamp in timestamps ]
        temp_info[channel]["Time Stamps"] = formatted_timestamps
    
    print(temp_info)

    # post processing: converting to pandas dataframe and converting to csv format

    df = pd.DataFrame.from_dict(temp_info)
    df.to_csv('TC08_Data.csv')

    return status

if __name__ == "__main__":

    # set length recording in seconds

    recording_period = 5
    sampling_interval_ms = 400

    record_data(recording_period, sampling_interval_ms)

