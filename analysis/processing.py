import os 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
    raw_data = data_class.data.astype(np.float64)
    temp_values = raw_data[:, 0]
    time_values_seconds = raw_data[:, 2] / (10 ** 6)
    return temp_values, time_values_seconds


def extract_GPIO_data(data_class):

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

    extracted_data = {
        "main_flow_meter": [Main_flow_meter_time_seconds, Main_flow_rate],
        "TB_motor": [TB_motor_time_seconds, TB_motor_state],
        "PIV_signal": [PIV_pulse_time_seconds, PIV_pulse_state],
        "Dye_Inject_Signal": [Dye_injection_time_seconds, Dye_injection_state],
        "branch_flow_meter": [Branch_flow_meter_time_seconds, Branch_flow_rate]
    }

    return extracted_data

def exponential_filter(x,alpha=0.3):

    s = np.zeros(len(x))

    s[0] = x[0]

    for t in range(1,len(x)):
        s[t] = alpha*x[t] + (1-alpha)*s[t-1]

    return s

def plot_flow_rate_GPIO_data():

    # quick an easy function for lab tuning 

    return 0 

def create_dataclasses_for_run(run_folder_path, angles):

    test_runs = []
    
    # Obtain the CSV Files and create dataclasses for each test run with that inlet condition

    for index, test_run in enumerate(os.scandir(folder_path)):
        if test_run.name == '.DS_Store' or not test_run.is_dir():
            continue  # Skip .DS_Store file and non-directories

        subfolder_path = test_run.path
        print(f'Processing run at: {subfolder_path}')

        # append all classes in a list called test_runs 

        test_runs.append(process_individual_run(subfolder_path, angle[index]))

    return test_runs 

def sort_test_runs(test_runs):

    test_bed_measurements = []
    
    four_mm = []
    
    three_mm = []
    
    two_mm = []
    
    one_mm = []
    
    temperatures = [] # contains all temperature measurements 
    
    GPIO_structs = []

    for run_number, run_info in enumerate(test_runs):
        for index, channels in enumerate(run_info):
            if channels.type == "temp":

                # If this is a pressure + testbed measurement:
                if channels.depth == null and (channels.rotation_angle - angle[
                    run_number]) != null and channels.location != null and channels.channel != "CHANNELCJC":
                    test_bed_measurements.append(channels)

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
            
                GPIO_structs.append(channels)

    for measurement in test_bed_measurements:

        measurement.print_status()


    sorted_structs = {"test_bed_measurements": test_bed_measurements, "four_mm": four_mm, "three_mm": three_mm, "two_mm": two_mm, "one_mm": one_mm, "GPIO_structs": GPIO_structs}

    return sorted_structs 

# def analyse_all_GPIO(GPIO_structs):

#     labels = ["main flow rate", "TB motor", "PIV", "Dye Inject", "Branch Flow"]
#     for i, struct in enumerate(GPIO_structs):

#         GPIO_run_data = extract_GPIO_data(struct)

#         for index, run_data in enumerate(GPIO_run_data):

#             plt.scatter(run_data[0], run_data[1], label=labels[index],s=1)
#             plt.title(f"{i}, GPIO Pin list {index} - Run")
#             plt.legend()

#             plt.show()

#     return {}

def analyse_GPIO_run_data(GPIO_struct):

    GPIO_run_data = extract_GPIO_data(GPIO_struct)

    # extracted_data = {
    #     "main_flow_meter": [Main_flow_meter_time_seconds, Main_flow_rate],
    #     "TB_motor": [TB_motor_time_seconds, TB_motor_state],
    #     "PIV_signal": [PIV_pulse_time_seconds, PIV_pulse_state],
    #     "Dye_Inject_Signal": [Dye_injection_time_seconds, Dye_injection_state],
    #     "branch_flow_meter": [Branch_flow_meter_time_seconds, Branch_flow_rate]
    # }

    filtered_branch = exponential_filter(GPIO_run_data["branch_flow_meter"][1])
    # filtered_main = exponential_filter(GPIO_run_data["main_flow_meter"][1])

    sns.set_theme()

    fig1, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8)) 
    axes[0].set_xlabel('Time (s)')
    axes[0].set_ylabel('Flow Rate (ml/s)')
    axes[0].set_title('Branch Flow Rates and Signals') 
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel('Flow Rate (ml/s)')
    axes[1].set_title('Main Flow Rates and Signals')    
    
    axes[0].legend(loc='best')
    axes[1].legend(loc='best')
    
    fig1.canvas.manager.set_window_title('Figure 1') 
    fig1.suptitle('Actual Flow Rates and Signals')   

    sns.scatterplot(x=GPIO_run_data["branch_flow_meter"][0], y=GPIO_run_data["branch_flow_meter"][1], ax=axes[0], label="Branch Flow Rate Raw", s=5, color="red")  

    for x in GPIO_run_data["TB_motor"][0]:

        axes[0].vlines(x, ymin=min(GPIO_run_data["branch_flow_meter"][1]), ymax=max(GPIO_run_data["branch_flow_meter"][1]), linestyle='--', linewidth=0.5)

    sns.scatterplot(x=GPIO_run_data["main_flow_meter"][0], y=GPIO_run_data["main_flow_meter"][1], ax=axes[1], label="Main Flow Rate Raw", s=5)
     
    # sns.lineplot(x=GPIO_run_data["main_flow_meter"][0], y=filtered_main, ax=axes, label="Main Flow Rate Filtered")  

    sns.lineplot(x=GPIO_run_data["branch_flow_meter"][0], y=filtered_branch, ax=axes[0], label="Branch Flow Rate Filtered")      
                
    plt.tight_layout()

    plt.show()

    return {}

def analyse_all_pico_data(processed_data):

    # sorted_structs = {"test_bed_measurements": test_bed_measurements, "four_mm": four_mm, "three_mm": three_mm, "two_mm": two_mm, "one_mm": one_mm, "GPIO_structs": GPIO_structs}

    test_bed_measurements = processed_data["test_bed_measurements"]
    four_mm = processed_data["four_mm"]
    three_mm = processed_data["three_mm"]
    two_mm = processed_data["two_mm"]
    one_mm = processed_data["one_mm"]

    # for measurement in test_bed_measurements: # rotation, depth, location 

    #     print(measurement.print_status())
    
    # for measurement in four_mm:

    #     print(measurement.print_status())

    # for measurement in three_mm:

    #     print(measurement.print_status())

    # for measurement in two_mm:

    #     print(measurement.print_status())

    # for measurement in one_mm:

    #     print(measurement.print_status())

    # def print_status(self):
    #     print("File name : " + self.filename)
    #     print("%s, %s" % (self.unit, self.channel))
    #     print("Rotation Angle : " + str(self.rotation_angle))
    #     print("Depth : " + str(self.depth) + " mm")
    #     print("Location : " + self.location)
    #     print("%s, %s" % (self.date, self.start_time))
    #     print("Type: " + self.type)

    # def print_data(self):
    #     print(self.data)


    return {}

def analyse_all_runs(folder_path, angle):

    # analysing all runs - to be done at the end of all measurements (12 or 8 rotations per inlet condition)

    test_runs = create_dataclasses_for_run(folder_path, angle)

    processed_data = sort_test_runs(test_runs)

    for i in range(len(test_runs)):

        analyse_GPIO_run_data(processed_data["GPIO_structs"][i])

        # analyse_all_pico_data(processed_data)

    return {}

def analyse_single_run():

    # on the spot running of data

    # analyse_GPIO_run_data(processed_data["GPIO_structs"]) i.e., not indexed in comparison to use in "analyse_all_runs"

    return {}

if __name__ == "__main__":

    # Looking at data for a particular inlet condition 

    angle = [0, 30, 60]  
    
    folder_path = 'analysis/data/opaque/inlet1'

    analyse_all_runs(folder_path, angle)
    
    analyse_single_run()






