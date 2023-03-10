from PySerial import list_ports

def find_ports():

    ports_available = list_ports()

    for port, index in enumerate(ports_available):
        print(f'SELECTION {port}: {index}')

    DAQ_port_index = int(input("Choose DAQ port selection number (input should be an integer): "))

    TB_port_index = int(input("Choose TB port selection number (input should be an integer): "))

    user_ports = {'DAQ': ports_available[DAQ_port_index], 'TB': ports_available[TB_port_index]}

    return user_ports

if __name__ == "__main__":

    print(find_ports())


