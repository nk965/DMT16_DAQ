import serial


def removePadding(string):

    for i in range(len(string)):  # Loop through the string input
        if i % 2 == 1:  # Every 2 elements, it has been padded by +1 so we remove the padding then de-convert
            ans += (int(bases[string[i]]) - 1) * \
                (pow(15, (len(string) - 1 - i)))
        else:  # Otherwise, standard conversion
            ans += int(bases[string[i]]) * \
                (pow(15, (len(string)-1-i)))

    return string


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

    ans = 0  # Temporary return val

    string = str(UART_output.hex())  # Convert back to hex string

    hex_identifier = string[:2]

    sampling_interval_hex = string[2:]

    result = removePadding(sampling_interval_hex)

    for i in range(len(sampling_interval_hex)):  # Loop through the string input
        if i % 2 == 1:  # Every 2 elements, it has been padded by +1 so we remove the padding then de-convert
            ans += (int(bases[sampling_interval_hex[i]]) - 1) * \
                (pow(15, (len(sampling_interval_hex) - 1 - i)))
        else:  # Otherwise, standard conversion
            ans += int(bases[sampling_interval_hex[i]]) * \
                (pow(15, (len(sampling_interval_hex)-1-i)))

    message = {
        "hex_identifier": hex_identifier,
        "sampling_interval_hex": sampling_interval_hex,
        "sampling_interval_ms": convert_to_ms(result)
    }

    return message


def convert_to_ms(sampling_interval_hex):

    actual = (((sampling_interval_hex - 0) * (5000 - 100)) /
              ((15**(8 // 4) - 1) - 0)) + 0

    return actual


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 230400, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            # .decode('utf-8').rstrip()
            line = convert_back_base_15(ser.readline())
            print(line)
