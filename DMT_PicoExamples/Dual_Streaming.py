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
from TC08_config import USBTC08_CONFIG, INPUT_TYPES

class LoggingUnit:
    
    def __init__(self, config, sampling_interval_input, recording_period) -> None:
        
        self.chandle = ctypes.c_int16(tc08.usb_tc08_open_unit())
        self.config = config
        self.sampling_interval_input = sampling_interval_input
        self.recording_period = recording_period
        self.status = {}

        ''' 
        logging unit initialisation procedure, non time sensitive
        '''

        # open unit
        self.status["handle"] = self.chandle
        
        # set mains rejection to 50 Hz
        self.status["set_mains"] = tc08.usb_tc08_set_mains(self.chandle, 0)

        # setting channels 

        self.status["set_channels"] = tc08.usb_tc08_set_channels(self.chandle, 0, INPUT_TYPES['K'])
        assert_pico2000_ok(status["set_channels"])

        for channel in self.config:

            if self.config[channel]["ENABLE"] == True:

                input_type = INPUT_TYPES[self.config[channel]['SENSOR_TYPE']]

                self.status["set_channel"] = tc08.usb_tc08_set_channel(self.chandle, self.config[channel]['CHANNEL_NO'], input_type)
                
                assert_pico2000_ok(self.status["set_channel"])

        # set sampling interval 

        self.status["interval_ms"] = self.sampling_interval_input if self.sampling_interval_input >= tc08.usb_tc08_get_minimum_interval_ms(self.chandle) else tc08.usb_tc08_get_minimum_interval_ms(self.chandle)

        assert_pico2000_ok(self.status["interval_ms"])

    def __repr__(self) -> str:

        ''' debugging function '''

        return f'{self.status}'

    def closeUnit(self) -> None:

        ''' closing unit '''

        self.status["close_unit"] = tc08.usb_tc08_close_unit(self.chandle)
        assert_pico2000_ok(self.status["close_unit"])

    def stopUnit(self) -> None:

        ''' stopping unit from running'''

        self.status["stop"] = tc08.usb_tc08_stop(self.chandle)
        assert_pico2000_ok(self.status["stop"])

    def runUnit(self) -> None:

        ''' start running unit at sampling frequency '''

        self.status["run"] = tc08.usb_tc08_run(self.chandle, self.status["interval_ms"]) 
        assert_pico2000_ok(self.status["run"])
        
        self.status["start_run_time"] = datetime.now()

    def setBuffers(self): 

        pass

    def pollData(self, temp_buffer, times_ms_buffer, BUFFER_SIZE, overflow, channel, info, results):

        self.status["get_temp"] = tc08.usb_tc08_get_temp_deskew(
            self.chandle, 
            ctypes.byref(temp_buffer), 
            ctypes.byref(times_ms_buffer),
            ctypes.c_int32(BUFFER_SIZE), 
            ctypes.byref(overflow), 
            info['CHANNEL_NO'], 
            0, 
            0
        )

        assert_pico2000_ok(self.status["get_temp"])

        return {}

        # results[channel]["Temperatures"] = np.asarray(temp_buffer)
        # results[channel]["Time Intervals"] = np.asarray(times_ms_buffer)
        # results[channel]["Overflow"] = overflow

        pass 


if __name__ == "__main__":

    # set length recording in seconds

    sns.set_theme(style="darkgrid")

    recording_period = 180
    polling_interval = 30
    sampling_interval_ms = 300

    results = {}

    UNIT_1 = LoggingUnit(USBTC08_CONFIG["UNIT_1"], sampling_interval_ms, recording_period)

    UNIT_2 = LoggingUnit(USBTC08_CONFIG["UNIT_2"], sampling_interval_ms, recording_period)

    UNIT_1.runUnit()
    UNIT_2.runUnit()

    ''' regularly poll for data (every 50 seconds) and add to dictionary temp_info '''

    current_time = 0

    while current_time < recording_period:
        
        if current_time + polling_interval <= recording_period:
        
            time.sleep(polling_interval)

            for logger in USBTC08_CONFIG:

                # collect data from each logger 

                results[logger] = {}

                for channel in USBTC08_CONFIG[logger]:

                        temp_buffer = (ctypes.c_float * (int(BUFFER_SIZE)))()
        
                        times_ms_buffer = (ctypes.c_int32 * int(BUFFER_SIZE))()
        
                        overflow = ctypes.c_int16()

                        results[logger][channel] = {}

                        # call poll data

                # append data to results

            current_time += polling_interval
        
        else:
            
            time.sleep(recording_period - current_time)

            # do same process as above

            current_time = recording_period
    
    UNIT_1.stopUnit()
    UNIT_2.stopUnit()

    UNIT_1.closeUnit()
    UNIT_2.closeUnit()

    print(UNIT_1.__repr__)
    print(UNIT_2.__repr__)