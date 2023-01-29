import ctypes
import numpy as np
import time
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
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
    
    time.sleep(recording_period/2)
    start_time = datetime.now()

    BUFFER_SIZE = math.ceil(recording_period / (status["run"] / 1000)) 

    temp_info = {}

    for index, (channel, info) in enumerate(USBTC08_CHANNELS.items()):

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

    for channel in temp_info:

        df = pd.DataFrame.from_dict(temp_info[channel])

        df.to_csv(channel + ' 1 Data.csv')


    
    
    time.sleep(recording_period/2)

    for index, (channel, info) in enumerate(USBTC08_CHANNELS.items()):

        temp_buffer_2 = (ctypes.c_float * (int(BUFFER_SIZE)))()
        
        times_ms_buffer_2 = (ctypes.c_int32 * int(BUFFER_SIZE))()
        
        overflow_2 = ctypes.c_int16()

        temp_info[channel] = {}

        status["get_temp"] = tc08.usb_tc08_get_temp_deskew(
            chandle, 
            ctypes.byref(temp_buffer_2), 
            ctypes.byref(times_ms_buffer_2),
            ctypes.c_int32(BUFFER_SIZE), 
            ctypes.byref(overflow_2), 
            info['CHANNEL_NO'], 
            0, 
            0
        )

        assert_pico2000_ok(status["get_temp"])

        temp_info[channel]["Temperatures_2"] = np.asarray(temp_buffer_2)
        temp_info[channel]["Time Intervals_2"] = np.asarray(times_ms_buffer_2)
        temp_info[channel]["Overflow_2"] = overflow_2

    # stop unit
    status["stop"] = tc08.usb_tc08_stop(chandle)
    assert_pico2000_ok(status["stop"])

    # close unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])
    print(status)

    # post processing: adding time stamps and converting to pandas DataFrame to save to csv format

    for channel in temp_info:

        start_timestamp = int(start_time.timestamp() * 1000)

        # add the intervals (in milliseconds) to the start timestamp
        #timestamps_ms = start_timestamp + temp_info[channel]["Time Intervals"]

        # convert the timestamps in ms to datetime
        #timestamps = [datetime.fromtimestamp(ts/1000) for ts in timestamps_ms]

        # format the timestamp
        #formatted_timestamps = [timestamp.strftime("%M:%S:%f") for timestamp in timestamps ]
        #temp_info[channel]["Time Stamps"] = formatted_timestamps

        # convert to dataframe and save as csv file

        df = pd.DataFrame.from_dict(temp_info[channel])

        df.to_csv(channel + ' 2 Data.csv')

        # iterate over the dictionary, adding the data for each channel to the dataframe
        
        #fig, ax = plt.subplots()
        
        #for channel, data in temp_info.items():
            #df = pd.DataFrame({'Time Intervals':data['Time Intervals'], 'Temperatures':data['Temperatures']})
           #sns.scatterplot(x=df['Time Intervals'], y=df['Temperatures'], label=channel, ax=ax)
        
    #plt.title('TC08 Temperature Data')
    
    #plt.xlabel('Time Interval (ms)')
    
    #plt.ylabel('Temperature (deg)')
    
    #plt.legend()
    
    #plt.show()

    return status

if __name__ == "__main__":

    # set length recording in seconds

    sns.set_theme(style="darkgrid")

    recording_period = 30
    sampling_interval_ms = 1

    record_data(recording_period, sampling_interval_ms)

