import serial
from RPI_config import inputInfo
from Streaming import streaming_data

def decode(string):

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

    string = str(UART.hex())  # Convert back to hex string

    substrings = []

    for i in range(0, len(string), 2):
        # extract a substring of length two and append it to the list
        substrings.append(string[i:i+2])

    return substrings

def SRPICommand(UART):

    hex_identifier = UART[0]

    sampling_interval_hex = UART[2:]

    decoded_sampling_interval = decode(sampling_interval_hex)

    sampling_interval_ms = convert_to_ms(decoded_sampling_interval)

    recording_period = 10 # TODO add interrupt

    status = streaming_data(sampling_interval_ms, recording_period) # Refactor to add interrupt

    message = {"hex_identifier": hex_identifier, "sampling_interval": sampling_interval_ms, "streaming_status": status}

    return message

def convert_to_ms(decoded_sampling_interval):

    min_sampling_interval, max_sampling_interval = inputInfo["Datafreq"]["range"][0], inputInfo["Datafreq"]["range"][1] 

    encoded_message_min = 0 

    encoded_message_max = 15**(inputInfo["Datafreq"]["bits"] // 4) - 1

    actual = (((decoded_sampling_interval - encoded_message_min) * (max_sampling_interval - min_sampling_interval)) /
              (encoded_message_max - encoded_message_min)) + min_sampling_interval

    return actual

if __name__ == '__main__':
    
    ser = serial.Serial('/dev/ttyS0', 230400, timeout=1)
    
    ser.reset_input_buffer()
    
    while True:
    
        if ser.in_waiting > 0:
            # .decode('utf-8').rstrip()
    
            UART_messages = split_UART(ser.readline())

            print(UART_messages)

            if UART_messages[0] == "05":
    
                SRPICommand(UART_messages)
    
            else:
    
                print("Do something else")
