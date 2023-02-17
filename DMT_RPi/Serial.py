import serial

def convert_back_base_15(UART_output):
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

    ans = 0 # Temporary return val

    string = str(UART_output.hex()) # Convert back to hex string

    for i in range(len(string)): # Loop through the string input
        if i%2 == 1: # Every 2 elements, it has been padded by +1 so we remove the padding then de-convert
            ans += (int(bases[string[i]]) - 1) * (pow(15, (len(string) - 1 - i)))
        else: # Otherwise, standard conversion
            ans += int(bases[string[i]])*(pow(15,(len(string)-1-i)))

    return ans


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 230400, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = convert_back_base_15(ser.readline()) #.decode('utf-8').rstrip()
            print(line)