import os 
import matplotlib.pyplot as plt
from data_structs import Datalogger_Data, GPIO_Data
from channel_info import channel_info, null

def process_individual_run(folder_path, angle):
    data_dump_experiment_path = folder_path

    experiment_data = []

    for filename in os.listdir(data_dump_experiment_path):

        if filename.endswith('.csv'):  # Filter CSV files
 
            file_path = os.path.join(data_dump_experiment_path, filename)

            filename_array = filename.split("-")

            if filename_array[0] == 'RPI':
                experiment_data.append(GPIO_Data(file_path))

            else:
                split_filename = filename.split("-")
                unit = split_filename[0]
                channel = split_filename[2]
                depth, initial_angle, location = channel_info[(unit, channel)]
                experiment_data.append(Datalogger_Data(file_path, depth, initial_angle + angle, location))

    return experiment_data

def extract_pico_data(data_class):
    import numpy as np
    raw_data = data_class.data.astype(np.float64)
    temp_values = raw_data[:, 0]
    time_values_seconds = raw_data[:, 2] / (10 ** 6)
    return temp_values, time_values_seconds


def extract_GPIO_data(data_class):
    import numpy as np

    def convert_pulses_to_flow_rate(times):
        flow_rates = []

        pulses_per_litre = 1920
        litres_per_pulse = 1 / pulses_per_litre

        for i, t in enumerate(times[:-1]):
            dt = times[i + 1] - times[i]
            flow_rate = litres_per_pulse / dt
            flow_rates.append(flow_rate)

        return flow_rates, times[:-1]

    # Main flow meter 1
    Main_flow_meter_data = data_class.Pin1_data

    # TB motor actuation 8
    TB_motor_data = data_class.Pin8_data

    # PIV Pulse 16
    PIV_pulse_data = data_class.Pin16_data

    # Dye injection actuation 20
    Dye_injection_data = data_class.Pin20_data

    # Branch Flow Meter 21
    Branch_flow_meter_data = data_class.Pin21_data

    if Main_flow_meter_data.size == 0:
        Main_flow_rate = []
        Main_flow_meter_time_seconds = []
    else:
        Main_flow_meter_state = Main_flow_meter_data[:, 1].astype(np.float64)
        Main_flow_meter_time_seconds = Main_flow_meter_data[:, 4].astype(np.float64) / (10 ** 6)
        Main_flow_rate, Main_flow_meter_time_seconds = convert_pulses_to_flow_rate(Main_flow_meter_time_seconds)

    if TB_motor_data.size == 0:
        TB_motor_state = []
        TB_motor_time_seconds = []
    else:
        TB_motor_state = TB_motor_data[:, 1].astype(np.float64)
        TB_motor_time_seconds = TB_motor_data[:, 4].astype(np.float64) / (10 ** 6)

    if PIV_pulse_data.size == 0:
        PIV_pulse_state = []
        PIV_pulse_time_seconds = []
    else:
        PIV_pulse_state = PIV_pulse_data[:, 1].astype(np.float64)
        PIV_pulse_time_seconds = PIV_pulse_data[:, 4].astype(np.float64) / (10 ** 6)

    if Dye_injection_data.size == 0:
        Dye_injection_state = []
        Dye_injection_time_seconds = []
    else:
        Dye_injection_state = Dye_injection_data[:, 1].astype(np.float64)
        Dye_injection_time_seconds = Dye_injection_data[:, 4].astype(np.float64) / (10 ** 6)

    if Branch_flow_meter_data.size == 0:
        Branch_flow_rate = []
        Branch_flow_meter_time_seconds = []
    else:
        Branch_flow_meter_state = Branch_flow_meter_data[:, 1].astype(np.float64)
        Branch_flow_meter_time_seconds = Branch_flow_meter_data[:, 4].astype(np.float64) / (10 ** 6)
        Branch_flow_rate, Branch_flow_meter_time_seconds = convert_pulses_to_flow_rate(Branch_flow_meter_time_seconds)

    return [[Main_flow_meter_time_seconds, Main_flow_rate], [TB_motor_time_seconds, TB_motor_state],
                       [PIV_pulse_time_seconds, PIV_pulse_state], [Dye_injection_time_seconds, Dye_injection_state],
                       [Branch_flow_meter_time_seconds, Branch_flow_rate]]

def exponential_filter(x,alpha=0.3):

    import numpy as np
    s = np.zeros(len(x))
    s[0] = x[0]

    for t in range(1,len(x)):
        s[t] = alpha*x[t] + (1-alpha)*s[t-1]

    return s

def plot_flow_rate_GPIO_data():



    return 0 

def plot_all_GPIO_data(GPIO_struct):

    labels = ["main flow rate", "TB motor", "PIV", "Dye Inject", "Branch Flow"]
    for i, struct in enumerate(GPIO_struct):

        GPIO_run_data = extract_GPIO_data(struct)

        for index, run_data in enumerate(GPIO_run_data):

            plt.scatter(run_data[0], run_data[1], label=labels[index],s=1)
            plt.title(f"{i}, GPIO Pin list {index} - Run")
            plt.legend()

            plt.show()

    return 0 

if __name__ == "__main__":

    # Looking at data for a particular inlet condition 

    angle = [0, 30, 60]  
    folder_path = 'analysis/data/opaque/inlet1'
    
    test_runs = []
    
    # Obtain the CSV Files and create dataclasses for each test run with that inlet condition

    for index, test_run in enumerate(os.scandir(folder_path)):
        if test_run.name == '.DS_Store' or not test_run.is_dir():
            continue  # Skip .DS_Store file and non-directories

        subfolder_path = test_run.path
        print(f'Processing run at: {subfolder_path}')

        # append all classes in a list called test_runs 

        test_runs.append(process_individual_run(subfolder_path, angle[index]))

    # intialise individual arrays for sorting algorithm

    pressures = []
    
    four_mm = []
    
    three_mm = []
    
    two_mm = []
    
    one_mm = []
    
    temperatures = [] # contains all temperature measurements 
    
    GPIO_struct = []

    for run_number, run_info in enumerate(test_runs):
        for index, channels in enumerate(run_info):
            if channels.type == "temp":

                # If this is a pressure measurement:
                if channels.depth == null and (channels.rotation_angle - angle[
                    run_number]) != null and channels.location != null and channels.channel != "CHANNELCJC":
                    pressures.append(channels)

                # Else, it must be a temperature measurement:
                else:
                    
                    temperatures.append(channels)

                    if channels.depth == 4:
                        four_mm.append(channels)
                    elif channels.depth == 3:
                        three_mm.append(channels)
                    elif channels.depth == 2:
                        two_mm.append(channels)
                    elif channels.depth == 1:
                        one_mm.append(channels)
            
            elif channels.type == "GPIO":
            
                GPIO_struct.append(channels)

    print(temperatures)

    for temp in temperatures:
        temp.print_status()
    
    plot_all_GPIO_data(GPIO_struct)

    GPIO_run_data_branch = extract_GPIO_data(GPIO_struct[0])[4]
    # print(GPIO_run_data_branch)

    filtered = exponential_filter(GPIO_run_data_branch[1])
    plt.plot(GPIO_run_data_branch[0], filtered, label="Filtered")
    plt.scatter(GPIO_run_data_branch[0], GPIO_run_data_branch[1], s=1, label="Unfiltered",color="r")
    plt.title("Filtered vs Unfiltered")
    plt.legend()
    plt.show()


