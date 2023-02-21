import serial
from RPI_config import inputInfo
from TC08_config import USBTC08_CONFIG, EXPERIMENT_CONFIG

"""
@author: Jimmy van de Worp
This script receieves and decodes two UART signals SPRI and SPRI2 and then reads these into a text file for GPIO.py and Streaming.py

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

    sampling_interval_hex = UART[1]

    decoded_sampling_interval = decode(sampling_interval_hex)

    sampling_interval_ms = convert_to_ms(decoded_sampling_interval)

    message = {"hex_identifier": hex_identifier, "sampling_interval": sampling_interval_ms}

    return message


def SRPI2_Read(UART):

    """This function reads the split UART list of strings and on the condition that it is SPRI2 calls the conversion function for the length of experiment

    Returns:
        list: list of hex identifier and length of experiment in s
    """   

    hex_identifier = UART[0]

    lenExperiment = UART[1] + UART [2]

    decoded_lenExperiment = decode(lenExperiment)

    lenExperiment_s = convert_to_s(decoded_lenExperiment)

    message = {"hex_identifier": hex_identifier, "Length of Experiment": lenExperiment_s}

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





def convert_to_s(decoded_len_experiment):

    """This function converts the decoded value of the sampling interval to the real value given the limitations of sending the data

    Returns:
        int: Integer value of the real sampling interval in ms
    """   

    min_len_experiment, max_len_experiment = inputInfo["lenExperiment"]["range"][0], inputInfo["lenExperiment"]["range"][1] 

    encoded_message_min = 0 

    encoded_message_max = 15**(inputInfo["lenExperiment"]["bits"] // 4) - 1

    actual = (((decoded_len_experiment - encoded_message_min) * (max_len_experiment - min_len_experiment)) /
              (encoded_message_max - encoded_message_min)) + min_len_experiment

    return actual





if __name__ == '__main__':
    
    ser = serial.Serial('/dev/ttyS0', 230400, timeout=1)
    
    ser.reset_input_buffer()

    counter = 0    
    
    while counter < 2:
    
        if ser.in_waiting > 0:
            # .decode('utf-8').rstrip()
    
            UART_messages = split_UART(ser.readline())

            print(UART_messages)

            if UART_messages[0] == "05":

                message = SRPI_Read(UART_messages)

                sampling_interval_ms = message["sampling_interval"]

                # extracts inputs from Serial.py and from configuration file

                polling_interval = EXPERIMENT_CONFIG['polling_interval']

                property_list = [str(sampling_interval_ms), str(polling_interval)]

                with open('SRPI.txt', 'w') as f:
                    for line in property_list:
                        f.write(line)
                        f.write('\n')
                
                counter +=1

            if UART_messages[0] == "10":

                message = SRPI2_Read(UART_messages)

                lenExperiment_s = message["Length of Experiment"]
                
                property_list = [str(lenExperiment_s)] 



                with open('SRPI.txt', 'a') as f:
                    for line in property_list:
                        f.write(line)
                        f.write('\n')       
                
                counter += 1

            else:
                print("Wrong")

