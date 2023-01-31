import ctypes
import numpy as np
import math
import pandas as pd
from datetime import datetime
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
from TC08_config import INPUT_TYPES

"""This contains the LoggingUnit class which is used in Streaming.py
It is an object which contains unit specific information as well as methods to collect data

"""


class LoggingUnit:

    def __init__(self, config, name, sampling_interval_input, recording_period) -> None:
        '''
        defining attributes of LoggingUnit class

        Attributes:
        chandle                     Unqiue identifier for unit for C API calls      
        name                        Name of the unit, e.g., "UNIT_1"
        config                      Dictionary of channels for specific unit with nested key-value pairs
        sampling_interval_input     User specified sampling interval in (ms)    
        recording_period            User specified recording period in (s) 
        status                      Pico Technology API call status (debugging)
        buffers                     Dictionary of keys (temp_buffers, buffer sizes, overflows) array of matrices

        '''

        self.chandle = ctypes.c_int16(tc08.usb_tc08_open_unit())  # opens unit
        self.name = name
        self.config = config
        self.sampling_interval_input = sampling_interval_input
        self.recording_period = recording_period
        self.status = {}
        self.buffers = {}

        # logging unit initialisation procedure, non time sensitive

        # assign unique identifier to status
        self.status["handle"] = self.chandle

        self.status["set_mains"] = tc08.usb_tc08_set_mains(
            self.chandle, 0)  # set mains rejection to 50 Hz

        # setting channels

        for channel in self.config:

            # iterate through channels from config, check if enabled and set them accordingly

            if self.config[channel]["ENABLE"] == True:

                # looks up type of sensor
                input_type = INPUT_TYPES[self.config[channel]['SENSOR_TYPE']]

                self.status["set_channel"] = tc08.usb_tc08_set_channel(
                    self.chandle, self.config[channel]['CHANNEL_NO'], input_type)

                # verifies API call is successful
                assert_pico2000_ok(self.status["set_channel"])

            else:

                # remove disabled channels from it's own configuation attributes
                del self.config[channel]

        # set sampling interval, check if user specified sampling interval is possible

        self.status["interval_ms"] = self.sampling_interval_input if self.sampling_interval_input >= tc08.usb_tc08_get_minimum_interval_ms(
            self.chandle) else tc08.usb_tc08_get_minimum_interval_ms(self.chandle)

        # verifies API call is successful
        assert_pico2000_ok(self.status["interval_ms"])

    def __repr__(self) -> str:
        ''' debugging function '''

        # returns status attribute which contains the results of the API calls (check Pico doumentation)
        return f'{self.status}'

    def closeUnit(self) -> None:
        ''' turns off and closes unit '''

        self.status["close_unit"] = tc08.usb_tc08_close_unit(self.chandle)
        assert_pico2000_ok(self.status["close_unit"])

    def stopUnit(self) -> None:
        ''' stops unit from running '''

        self.status["stop"] = tc08.usb_tc08_stop(self.chandle)
        # verifies API call is successful
        assert_pico2000_ok(self.status["stop"])

    def runUnit(self) -> None:
        ''' start running unit at sampling interval '''

        self.status["run"] = tc08.usb_tc08_run(
            self.chandle, self.status["interval_ms"])
        # verifies API call is successful
        assert_pico2000_ok(self.status["run"])

        # adds starting time stamp for timing
        self.status["start_run_time"] = datetime.now()

    def setBuffers(self, polling_period) -> None:
        ''' initialise dictionary of buffers for polling 
        TC08 requires polling of data every 50 seconds and copies data per poll to a specific buffer memory location
        Data structure schema is as follows:

        buffers = {
            "temp_buffers": [
                [ [22.7, 33.2], [24, 33.2], [33.5, 33.1] ], # poll 1: Channel 1, Channel 2, Channel 3
                [ [22.6, 31.9], [24, 33.2], [33.8, 33.8] ], # poll 2: Channel 1, Channel 2, Channel 3
                [ [22.1, 35.3], [24, 33.2], [33.5, 33.1] ], # poll 3: Channel 1, Channel 2, Channel 3
                [ [22.2, 33.2], [24, 33.2], [33.5, 33.1] ], # poll 4: Channel 1, Channel 2, Channel 3
            ]
            "times_ms_buffers": [
                ...
            ]
        }

        '''
        self.buffers["temp_buffers"] = []
        self.buffers["times_ms_buffers"] = []
        self.buffers["buffer_sizes"] = []
        self.buffers["overflows"] = []

        for poll in polling_period:

            # size of each buffer (array) determined by polling time
            BUFFER_SIZE = math.ceil(poll / (self.status["interval_ms"] / 1000))

            self.buffers["temp_buffers"].append(
                (ctypes.c_float * (int(BUFFER_SIZE)) * int(len(self.config)))())  # creation of matrix of buffer size x number of channels

            self.buffers["times_ms_buffers"].append(
                (ctypes.c_int32 * int(BUFFER_SIZE) * int(len(self.config)))())  # creation of matrix of buffer size x number o channels

            # not matrix, array of buffer sizes
            self.buffers["buffer_sizes"].append(BUFFER_SIZE)

            # assigns memory location for overflows (necessary for Pico docs)
            self.buffers["overflows"].append(ctypes.c_int16())

    def pollData(self, polling_index) -> None:
        ''' polls data for all channels for this unit '''

        for index, info in enumerate(self.config.values()):

            self.status["get_temp"] = tc08.usb_tc08_get_temp_deskew(
                self.chandle,  # specifies unique identifier for
                ctypes.byref(
                    self.buffers["temp_buffers"][polling_index][index]),  # specifies memory location to write temperature data
                ctypes.byref(
                    self.buffers["times_ms_buffers"][polling_index][index]),  # specifies memory location to write times data
                ctypes.c_int32(self.buffers["buffer_sizes"][polling_index]), # specifies buffer size
                ctypes.byref(self.buffers["overflows"][polling_index]), # specifies memory location for overflow
                info['CHANNEL_NO'], # specifies channel number to read data from
                0,  # units in centigrade (check Pico Technology documentation)
                0  # fills missing values with QNaNs
            )

        # verifies API call is successful
        assert_pico2000_ok(self.status["get_temp"])

    def overflowCheck(self) -> dict:
        ''' debugging purposes to check if overflow has occured (data out of range) '''

        return {f'{self.buffers["overflows"]}'}

    def grabData(self) -> dict:

        ''' returns data (info) in the form of a dictionary and plots
        
        info has the following schema: 

        info = {
            "Name": UNIT_1,
            "Start": datetime.datetime() 
            "Raw Data": {
                "CHANNEL 1": {
                    "temp_buffers": [ 11, 12, 14, 15],
                    "times_ms_buffers": [0, 1000, 2000, 3000],
                    "Time Stamps": [ ... ],
                }, 
                "CHANNEL 2": {
                    ...
                }
            } 
        }
        
        '''

        info = {"Name": self.name, "Start": self.status["start_run_time"]}

        raw_data = {}

        output_data = ["temp_buffers", "times_ms_buffers"]

        for index, channel in enumerate(self.config.keys()):

            # iterating through enabled channels

            raw_data[channel] = {}

            for data in output_data:

                # populating channel specific data

                raw_data[channel][data] = {}

                # initalise numpy array

                polled_data = np.asarray(self.buffers[data][0][index])

                for i in range(1, len(self.buffers[data])):

                    polled_data = np.concatenate(
                        (polled_data, np.asarray(self.buffers[data][i][index])))

                raw_data[channel][data] = polled_data

            # generate time stamps

            start_timestamp = int(info["Start"].timestamp() * 1000)

            # add the intervals (in milliseconds) to the start timestamp

            timestamps_ms = start_timestamp + \
                raw_data[channel]["times_ms_buffers"]

            # convert the timestamps in ms to datetime

            timestamps = [datetime.fromtimestamp(
                ts/1000) for ts in timestamps_ms]

            # format the timestamp

            formatted_timestamps = [timestamp.strftime(
                "%H:%M:%S:%f") for timestamp in timestamps]

            raw_data[channel]["Time Stamps"] = formatted_timestamps

            # create pandas dataframe and export to csv

            df = pd.DataFrame.from_dict(raw_data[channel])

            filename = f"{self.name}_{channel} Data.csv"

            df.to_csv(filename)
        
        info["raw_data"] = raw_data 

        return info
