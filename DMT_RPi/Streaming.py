import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from TC08_config import USBTC08_CONFIG, EXPERIMENT_CONFIG
from TC08_unit import LoggingUnit

"""
@author: Nicholas Kwok
This script performs streaming mode for a specified recording period, polling interval and sampling interval (ms).
It initialises the LoggingUnit object per logger used. 
"""

def getPolling_Period(recording_period, polling_interval):

    """obtains an array of polling intervals
    Returns:
        array: array of duration of time.sleep
    """    

    current_time = 0

    polling_period = []

    while current_time < recording_period:
        interval = min(polling_interval, recording_period - current_time)
        polling_period.append(interval)
        current_time += interval

    return polling_period

def plot_data(logger_data):

    """plots data for all loggers """  

    # iterates through all loggers

    for logger in logger_data:

        # extracts and plots channel as individual series

        for channel, data in logger["raw_data"].items():
            df = pd.DataFrame(
                {'times_ms_buffers': data['times_ms_buffers'], 'temp_buffers': data['temp_buffers']})

            sns.scatterplot(x=df['times_ms_buffers'],
                y=df['temp_buffers'], label=channel)

        plt.title(f'TC08 Temperature Data {logger["Name"]}')

        plt.xlabel('Time Interval (ms)')

        plt.ylabel('Temperature (deg)')

        plt.legend()

        plt.show()


def streaming_data():

    # extracts user inputs from text file

    x = []
    file_in = open('SRPI.txt', 'r')
    for line in file_in.readlines():
        x.append(float(line))
    file_in.close()

    sampling_interval_ms, recording_period, polling_interval = x[0], x[1], x[2]

    # defining array to be populated with LoggingUnit objects

    loggers = []

    # initialises and starts the TC08 loggers (LED to blink green)

    for name, logger_info in USBTC08_CONFIG.items():
        loggers.append(LoggingUnit(logger_info, name,
                       sampling_interval_ms, recording_period))

    # creates array of polling intervals to loop through 

    polling_period = getPolling_Period(recording_period, polling_interval)

    # non time sensitive setting of buffers 

    for logger in loggers:
        logger.setBuffers(polling_period)

    # extracts inputs from Serial.py and from configuration file

    # extracts user inputs from text file

    x = []
    file_in = open('SRPI.txt', 'r')
    for line in file_in.readlines():
        x.append(float(line))
    file_in.close()

    sampling_interval_ms, recording_period, polling_interval = x[0], x[1], x[2]

    # defining array to be populated with LoggingUnit objects

    loggers = []

    # initialises and starts the TC08 loggers (LED to blink green)

    for name, logger_info in USBTC08_CONFIG.items():
        loggers.append(LoggingUnit(logger_info, name,
                       sampling_interval_ms, recording_period))

    # creates array of polling intervals to loop through 

    polling_period = getPolling_Period(recording_period, polling_interval)

    # non time sensitive setting of buffers 

    for logger in loggers:
        logger.setBuffers(polling_period)

    # runs unit and time stamps are marked in method

    for logger in loggers:
        logger.runUnit()

    # regularly polls for data and saves it in buffer attribute

    for index, poll in enumerate(polling_period):

        time.sleep(poll)

        for logger in loggers:
            logger.pollData(index)

    # stops logger and print final status for debugging

    logger_data = []

    for logger in loggers:
        logger.stopUnit()
        logger.closeUnit()
        logger_data.append(logger.grabData())

    plot_data(logger_data)