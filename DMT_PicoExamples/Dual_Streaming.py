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
from TC08_config import USBTC08_CONFIG, INPUT_TYPES, EXPERIMENT_CONFIG

class LoggingUnit:
    
    def __init__(self, config, name, sampling_interval_input, recording_period) -> None:
        
        self.chandle = ctypes.c_int16(tc08.usb_tc08_open_unit())
        self.name = name
        self.config = config
        self.sampling_interval_input = sampling_interval_input
        self.recording_period = recording_period
        self.status = {}
        self.buffers = {}

        ''' 
        logging unit initialisation procedure, non time sensitive
        '''

        # open unit
        self.status["handle"] = self.chandle
        
        # set mains rejection to 50 Hz
        self.status["set_mains"] = tc08.usb_tc08_set_mains(self.chandle, 0)

        # setting channels 

        for channel in self.config:

            if self.config[channel]["ENABLE"] == True:

                input_type = INPUT_TYPES[self.config[channel]['SENSOR_TYPE']]

                self.status["set_channel"] = tc08.usb_tc08_set_channel(self.chandle, self.config[channel]['CHANNEL_NO'], input_type)
                
                assert_pico2000_ok(self.status["set_channel"])
            
            else: 
                
                del self.config[channel]

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

        ''' stopping unit from running '''

        self.status["stop"] = tc08.usb_tc08_stop(self.chandle)
        assert_pico2000_ok(self.status["stop"])

    def runUnit(self) -> None:

        ''' start running unit at sampling frequency '''

        self.status["run"] = tc08.usb_tc08_run(self.chandle, self.status["interval_ms"]) 
        assert_pico2000_ok(self.status["run"])
        
        self.status["start_run_time"] = datetime.now()
    
    def setBuffers(self, polling_period) -> None:

        self.buffers["temp_buffers"] = []
        self.buffers["times_ms_buffers"] = []
        self.buffers["buffer_sizes"] = []
        self.buffers["overflows"] = []

        for poll in polling_period:

            BUFFER_SIZE = math.ceil(poll / (self.status["interval_ms"] / 1000))

            self.buffers["temp_buffers"].append((ctypes.c_float * (int(BUFFER_SIZE)) * int(len(self.config)))()) 

            self.buffers["times_ms_buffers"].append((ctypes.c_int32 * int(BUFFER_SIZE) * int(len(self.config)))())

            self.buffers["buffer_sizes"].append(BUFFER_SIZE)

            self.buffers["overflows"].append(ctypes.c_int16())
 
    def pollData(self, polling_index):

        ''' polls data for all channels for this unit '''

        for index, info in enumerate(self.config.values()):

            self.status["get_temp"] = tc08.usb_tc08_get_temp_deskew(
            self.chandle, 
            ctypes.byref(self.buffers["temp_buffers"][polling_index][index]), 
            ctypes.byref(self.buffers["times_ms_buffers"][polling_index][index]),
            ctypes.c_int32(self.buffers["buffer_sizes"][polling_index]), 
            ctypes.byref(self.buffers["overflows"][polling_index]), 
            info['CHANNEL_NO'], 
            0, 
            0
        )

        assert_pico2000_ok(self.status["get_temp"])

    def overflowCheck(self):

        return {f'{self.buffers["overflows"]}'}
    
    def grabData(self):

        info = {}

        output_data = ["temp_buffers", "times_ms_buffers"]

        for index, channel in enumerate(self.config.keys()):

            # Iterates through the channels
            
            info[channel] = {}

            for data in output_data:

                polled_data = np.asarray(self.buffers[data][0][index])

                for i in range(1, len(self.buffers[data])):

                    polled_data = np.concatenate((polled_data, np.asarray(self.buffers[data][i][index])))

                info[channel] = {data: polled_data}

        return info




if __name__ == "__main__":

    # set length recording in seconds

    sns.set_theme(style="darkgrid")

    recording_period, polling_interval, sampling_interval_ms = EXPERIMENT_CONFIG['recording_period'], EXPERIMENT_CONFIG['polling_interval'], EXPERIMENT_CONFIG['sampling_interval_ms']

    current_time = 0

    polling_period = []

    while current_time < recording_period: 
        interval = min(polling_interval, recording_period - current_time)
        polling_period.append(interval)
        current_time += interval

    loggers = []

    for name, logger_info in USBTC08_CONFIG.items():
        loggers.append(LoggingUnit(logger_info, name, sampling_interval_ms, recording_period))
    
    for logger in loggers:
        logger.setBuffers(polling_period)

    for logger in loggers: 
        logger.runUnit()

    for index, poll in enumerate(polling_period):

        time.sleep(poll) 

        for logger in loggers:
            logger.pollData(index)

    for logger in loggers: 
        logger.stopUnit()
        logger.closeUnit()
        print(logger.grabData())
        print(logger.__repr__)

    # post processing

    #results = {}

    #for logger in loggers:
        #results[logger.name] = {}

        #temp_buffers = np.matrix(logger.buffers["temp_buffers"]) # FIXME: problem here 
        #times_ms_buffers = np.matrix(logger.buffers["times_ms_buffers"]) # FIXME: problem here

        #for index, channel in enumerate(loggers.config.keys()):

            #results[logger.name][channel] = {"Temperatures": temp_buffers[:, index].flatten()}
            #results[logger.name][channel] = {"Time Intervals": times_ms_buffers[:, index].flatten()}

    #print(results)







