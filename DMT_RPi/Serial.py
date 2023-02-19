import serial
import threading
import sys
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pigpio  # Library for high speed gpio
from RPI_config import inputInfo
from TC08_config import USBTC08_CONFIG, EXPERIMENT_CONFIG
from TC08_unit import LoggingUnit

"""
@author: Jimmy van de Worp
This script operates 3 threads:

Thread 1: thread_data_stream
    This thread performs streaming mode for a specified recording period, polling interval and sampling interval (ms).
    It initialises the LoggingUnit object per logger used. 

TODO: Thread 2: thread_GPIO    
    This thread receives high speed GPIO indefinitely and records the Pin Number, State, and Tick of each GPIO change detected

Thread 3: thread_EPRI
    This thread will close thread 1 and 2 upon receival of UART command EPRI

"""





def decode(string):

    """This function decodes a string from UART in base 15 hex string to an integer value whilst padding

    Returns:
        int: resulting value after conversion and padding
    """    

    bases = {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "a": "10",
        "b": "11",
        "c": "12",
        "d": "13",
        "e": "14",
        "f": "15"
    }

    result = 0

    for i in range(len(string)):  # Loop through the string input
        if i % 2 == 1:  # Every 2 elements, it has been padded by +1 so we remove the padding then de-convert
            result += (int(bases[string[i]]) - 1) * \
                (pow(15, (len(string) - 1 - i)))
        else:  # Otherwise, standard conversion
            result += int(bases[string[i]]) * \
                (pow(15, (len(string)-1-i)))

    return result





def split_UART(UART):

    """This function acts to split the UART into the hex indenifier and any following additional information

    Returns:
        list: list of the seperated substrings
    """    

    string = str(UART.hex())  # Convert back to hex string

    substrings = []

    for i in range(0, len(string), 2):
        # extract a substring of length two and append it to the list
        substrings.append(string[i:i+2])

    return substrings





def SRPI_Read(UART):

    """This function reads the split UART list of strings and on the condition that it is SPRI calls the conversion function for the sampling interval

    Returns:
        list: list of hex identifier and sampling interval in ms
    """   

    hex_identifier = UART[0]

    sampling_interval_hex = UART[2:]

    decoded_sampling_interval = decode(sampling_interval_hex)

    sampling_interval_ms = convert_to_ms(decoded_sampling_interval)

    message = {"hex_identifier": hex_identifier, "sampling_interval": sampling_interval_ms}

    return message





def convert_to_ms(decoded_sampling_interval):

    """This function converts the decoded value of the sampling interval to the real value given the limitations of sending the data

    Returns:
        int: Integer value of the real sampling interval in ms
    """   

    min_sampling_interval, max_sampling_interval = inputInfo["Datafreq"]["range"][0], inputInfo["Datafreq"]["range"][1] 

    encoded_message_min = 0 

    encoded_message_max = 15**(inputInfo["Datafreq"]["bits"] // 4) - 1

    actual = (((decoded_sampling_interval - encoded_message_min) * (max_sampling_interval - min_sampling_interval)) /
              (encoded_message_max - encoded_message_min)) + min_sampling_interval

    return actual





def logger_stop(loggers):

    """This function closes the dataloggers and calls for the data to be stored and recorded
     
    Returns:
        array: the array of the status for each logger """
    
    # stops logger and print final status for debugging
    
    logger_data = []
    logger_status = []

    for logger in loggers:
        logger.stopUnit()
        logger.closeUnit()
        logger_status.append(logger.__repr__())
        logger_data.append(logger.grabData())

    plot_data(logger_data)

    return logger_status





def getPolling_Period(recording_period, polling_interval):

    """This function obtains an array of polling intervals

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

    """This function plots data for all loggers """  

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





def streaming_data(loggers, polling_period):

    """This function runs the dataloggers and calls for the loggers to stop and close after set period"""    

    # runs unit and time stamps are marked in method

    for logger in loggers:
        logger.runUnit()

    # regularly polls for data and saves it in buffer attribute

    for index, poll in enumerate(polling_period):

        time.sleep(poll)

        for logger in loggers:
            logger.pollData(index)

    logger_stop(loggers)





def ERPI(loggers):

    """This function constantly pulls in UART for the ending procedure and then calls for the dataloggers to close """   

    if ser.in_waiting > 0:
        
        UART_messages = split_UART(ser.readline())
        
        print(UART_messages)

        if UART_messages[0] == "0D" or "0E":

            logger_stop(loggers)
        
        else:

            print('THIS IS A PROBLEM')










if __name__ == '__main__':
    
    ser = serial.Serial('/dev/ttyS0', 230400, timeout=1)
    
    ser.reset_input_buffer()    
    
    while True:
    
        if ser.in_waiting > 0:
            # .decode('utf-8').rstrip()
    
            UART_messages = split_UART(ser.readline())

            print(UART_messages)

            if UART_messages[0] == "05":

                message = SRPI_Read(UART_messages)

                sampling_interval_ms = message["sampling_interval"]
            
                # Initialise recording_period to be extremely high

                recording_period = 3600 # 1hr 

                # extracts inputs from Serial.py and from configuration file

                polling_interval = EXPERIMENT_CONFIG['polling_interval']

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
                
                thread_data_stream = threading.Thread(target = streaming_data(loggers, polling_period))
                #thread_GPIO = threading.Thread(target = GPIO)
                thread_ERPI = threading.Thread(target = ERPI(loggers))
                
                thread_data_stream.start()
                thread_ERPI.start()

    
            else:
    
                print("Do something else")
