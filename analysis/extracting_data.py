import os 
import numpy as np
from data_structs import Datalogger_Data, GPIO_Data
from channel_info import channel_info, null
from datetime import datetime

def process_individual_run(folder_path, angle=null):
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

    experiment_data.sort(key=lambda x: os.path.getctime(x.file_path))

    print(f"Analysing: {experiment_data}")

    return experiment_data

def extract_pico_data(data_class):
    raw_data = data_class.data.astype(np.float64)
    temp_values = raw_data[:, 0]
    time_values_seconds = raw_data[:, 2] / (10 ** 6)
    return temp_values, time_values_seconds


def extract_GPIO_data(data_class):

    def convert_pulses_to_flow_rate(times):
        flow_rates = []

        pulses_per_litre = 1530
        litres_per_pulse = 1 / pulses_per_litre

        for i, t in enumerate(times[:-1]):
            dt = times[i + 1] - times[i]
            flow_rate = litres_per_pulse / abs(dt)
            flow_rates.append(flow_rate * 1000)

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

    # Find time = 0, defined as when the transient condition starts, i.e., pin 8 (testbed motor actuation)

    if TB_motor_data.size == 0:
        TB_motor_state = []
        TB_motor_time_seconds = []
        time_0_reference = 0 
    else:
        TB_motor_state = TB_motor_data[:, 1].astype(np.float64)
        TB_motor_time_seconds = TB_motor_data[:, 4].astype(np.float64) / (10 ** 6)
        time_0_reference = TB_motor_data[:, 4].astype(np.float64)[0] / (10 ** 6)
        TB_motor_time_seconds = TB_motor_time_seconds - time_0_reference
    
    if Main_flow_meter_data.size == 0:
        Main_flow_rate = []
        Main_flow_meter_time_seconds = []
    else:
        Main_flow_meter_state = Main_flow_meter_data[:, 1].astype(np.float64)
        Main_flow_meter_time_seconds = Main_flow_meter_data[:, 4].astype(np.float64) / (10 ** 6) - time_0_reference
        Main_flow_rate, Main_flow_meter_time_seconds = convert_pulses_to_flow_rate(Main_flow_meter_time_seconds)

    if PIV_pulse_data.size == 0:
        PIV_pulse_state = []
        PIV_pulse_time_seconds = []
    else:
        PIV_pulse_state = PIV_pulse_data[:, 1].astype(np.float64)
        PIV_pulse_time_seconds = PIV_pulse_data[:, 4].astype(np.float64) / (10 ** 6) - time_0_reference

    if Dye_injection_data.size == 0:
        Dye_injection_state = []
        Dye_injection_time_seconds = []
    else:
        Dye_injection_state = Dye_injection_data[:, 1].astype(np.float64)
        Dye_injection_time_seconds = Dye_injection_data[:, 4].astype(np.float64) / (10 ** 6) - time_0_reference

    if Branch_flow_meter_data.size == 0:
        Branch_flow_rate = []
        Branch_flow_meter_time_seconds = []
    else:
        Branch_flow_meter_state = Branch_flow_meter_data[:, 1].astype(np.float64)
        Branch_flow_meter_time_seconds = Branch_flow_meter_data[:, 4].astype(np.float64) / (10 ** 6) - time_0_reference
        Branch_flow_rate, Branch_flow_meter_time_seconds = convert_pulses_to_flow_rate(Branch_flow_meter_time_seconds)

    time_string = data_class.start_time
    time_format = "%H_%M_%S"

    # Convert the string to a datetime object
    time_obj = datetime.strptime(time_string, time_format)

    # Format the datetime object as a nicer string
    presentable_time = time_obj.strftime("%I:%M:%S %p")

    extracted_data = {
        "main_flow_meter": [Main_flow_meter_time_seconds, Main_flow_rate],
        "TB_motor": [TB_motor_time_seconds, TB_motor_state],
        "PIV_signal": [PIV_pulse_time_seconds, PIV_pulse_state],
        "Dye_Inject_Signal": [Dye_injection_time_seconds, Dye_injection_state],
        "branch_flow_meter": [Branch_flow_meter_time_seconds, Branch_flow_rate],
        "time": presentable_time,
        "time_0_reference": time_0_reference
    }

    return extracted_data

def create_dataclasses_for_run(run_folder_path, angles):

    test_runs = []
    
    # Obtain the CSV Files and create dataclasses for each test run with that inlet condition

    for index, test_run in enumerate(os.scandir(run_folder_path)):
        if test_run.name == '.DS_Store' or not test_run.is_dir():
            continue  # Skip .DS_Store file and non-directories

        subfolder_path = test_run.path
        print(f'Processing run at: {subfolder_path}')

        # append all classes in a list called test_runs 

        test_runs.append(process_individual_run(subfolder_path, angles[index]))

    return test_runs 

def sort_test_runs(test_runs, angles):

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
                if channels.depth == null and (channels.rotation_angle - angles[
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

    pressures = []
    test_bed_temps = []

    for measurement in test_bed_measurements:

        if measurement.channel == "CHANNEL1" or measurement.channel== "CHANNEL2": 

            pressures.append(measurement)

        else:

            test_bed_temps.append(measurement)

    sorted_structs = {"pressures": pressures, "test_bed_temps": test_bed_temps, "four_mm": four_mm, "three_mm": three_mm, "two_mm": two_mm, "one_mm": one_mm, "GPIO_structs": GPIO_structs}

    return sorted_structs 







