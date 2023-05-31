import os 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

from scipy.fft import fft, fftfreq

from extracting_data import extract_GPIO_data, create_dataclasses_for_run, sort_test_runs, process_individual_run, extract_pico_data

sns.set_theme()

def exponential_filter(x,alpha=0.1):

    s = np.zeros(len(x))

    s[0] = x[0]

    for t in range(1,len(x)):
        s[t] = alpha*x[t] + (1-alpha)*s[t-1]

    return s

def plot_flow_rate_GPIO_data():

    # quick an easy function for lab tuning 

    return 0 

def analyse_GPIO_run_data(GPIO_struct):

    GPIO_run_data = extract_GPIO_data(GPIO_struct)

    filtered_branch = exponential_filter(GPIO_run_data["branch_flow_meter"][1])
    # filtered_main = exponential_filter(GPIO_run_data["main_flow_meter"][1])

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

    # for x in GPIO_run_data["TB_motor"][0]:

    #     axes[0].vlines(x, ymin=min(GPIO_run_data["branch_flow_meter"][1]), ymax=max(GPIO_run_data["branch_flow_meter"][1]), linestyle='--', linewidth=0.5)

    sns.scatterplot(x=GPIO_run_data["main_flow_meter"][0], y=GPIO_run_data["main_flow_meter"][1], ax=axes[1], label="Main Flow Rate Raw", s=5)
     
    # sns.lineplot(x=GPIO_run_data["main_flow_meter"][0], y=filtered_main, ax=axes, label="Main Flow Rate Filtered")  

    sns.lineplot(x=GPIO_run_data["branch_flow_meter"][0], y=filtered_branch, ax=axes[0], label="Branch Flow Rate Filtered")      
                
    plt.tight_layout()

    plt.show()

    return {}

def analyse_all_pico_data(processed_data):

    # TO BE COMPLETED, IDEAS INCLUDE FFT, PSD, POLAR PLOT, TEMP DISTRIBUTION INTERPOLATION

    # sorted_structs = {"pressures": pressures, "test_bed_temps": test_bed_temps, "four_mm": four_mm, "three_mm": three_mm, "two_mm": two_mm, "one_mm": one_mm, "GPIO_structs": GPIO_structs}


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

def plot_run_pico_data(pico_single_run_data, run_info):

    pressures = []
    opaque_temps = []
    test_bed_temps = []

    for measurement in pico_single_run_data:

        if (measurement.channel == "CHANNEL1" or measurement.channel== "CHANNEL2") and measurement.unit == "UNIT2": 

            pressures.append(measurement)

        if measurement.unit == "UNIT1":

            opaque_temps.append(measurement)

        else:

            test_bed_temps.append(measurement)

    def plot_pressures(pressures):

        # plot presssures side by side

        fig1, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
        
        for index, data in enumerate(pressures):

            axes[index].set_title(f'{data.location} Ring: Pressure vs Time')
            axes[index].set_xlabel('Time (s)')
            axes[index].set_ylabel('Pressure (mV)')

            temp_values, time_values_seconds = extract_pico_data(data)

            sns.scatterplot(x=time_values_seconds, y=temp_values, ax=axes[index], s=10)
        
        fig1.canvas.manager.set_window_title('PRESSURES') 
        
        fig1.suptitle(f'Pressures vs Time, CONDITIONS: {run_info["momentum_ratio_no"]}, at {run_info["temperature_string"]} at Orientation: {run_info["orientation"]} Pressures vs Time')

        fig1.subplots_adjust(wspace=0.3)

        plt.show()

    def plot_opaque_temperatures(opaque_temps):

        # plot temperatures as seperate plots 

        fig2, axes1 = plt.subplots(nrows=3, ncols=3, figsize=(15, 8))

        matrix = [opaque_temps[i:i+3] for i in range(0, 9, 3)]

        for i in range(len(matrix)):

            for j in range(len(matrix)):

                axes1[i][j].set_title(f'{matrix[i][j].depth} mm, {matrix[i][j].channel} at {matrix[i][j].rotation_angle} degrees')
                axes1[i][j].set_xlabel('Time (s)')
                axes1[i][j].set_ylabel('Temperature (degrees)')

                temp_values, time_values_seconds = extract_pico_data(matrix[i][j])

                sns.scatterplot(x=time_values_seconds, y=temp_values, ax=axes1[i][j], s=5)
        
        fig2.canvas.manager.set_window_title('TEMPERATURES') 
        
        fig2.suptitle(f'Temperature vs Time, CONDITIONS: {run_info["momentum_ratio_no"]}, at {run_info["temperature_string"]} at Orientation: {run_info["orientation"]} Pressures vs Time')

        plt.subplots_adjust(hspace=0.5)

        plt.show()

    def plot_testbed_temperatures(test_bed_temps):

        fig3, axes1 = plt.subplots(nrows=2, ncols=3, figsize=(15, 6))

        matrix = [test_bed_temps[i*3:(i+1)*3] for i in range(2)]

        for i in range(len(matrix)):

            for j in range(len(matrix[0])):

                axes1[i][j].set_title(f'{matrix[i][j].depth} mm, {matrix[i][j].channel} at {matrix[i][j].rotation_angle} degrees')
                axes1[i][j].set_xlabel('Time (s)')
                axes1[i][j].set_ylabel('Temperature (degrees)')

                temp_values, time_values_seconds = extract_pico_data(matrix[i][j])

                sns.scatterplot(x=time_values_seconds, y=temp_values, ax=axes1[i][j], s=5)
        
        fig3.canvas.manager.set_window_title('TESTBED TEMPERATURES') 
        
        fig3.suptitle(f'Testbed Temperature vs Time, CONDITIONS: {run_info["momentum_ratio_no"]}, at {run_info["temperature_string"]} at Orientation: {run_info["orientation"]} Pressures vs Time')

        plt.subplots_adjust(hspace=0.5)

        plt.show()

    plot_pressures(pressures)
    plot_opaque_temperatures(opaque_temps)
    plot_testbed_temperatures(test_bed_temps)

def analyse_single_run(run_folder_path, angle):

    # on the spot running of data

    experiment_data = process_individual_run(run_folder_path, angle)

    pico_single_run_data = []
    gpio_single_run_data = []

    # sort for unit, GPIO

    for data in experiment_data: 

        if data.type != "temp":

            gpio_single_run_data.append(data)

        else:

            pico_single_run_data.append(data)

    # plot temperatures/pressures and GPIO signals 

    split_array = run_folder_path.split("/")


    date_string = split_array[3]
    orientation_string = split_array[4].upper() + " " + split_array[5].upper()
    temperature_string = split_array[7] + " DEGREES"
    momentum_ratio_no_string = "RATIO " + split_array[9]

    run_info = {
        "date": date_string,
        "orientation": orientation_string,
        "temperature": temperature_string,
        "momentum_ratio_no": momentum_ratio_no_string,
    }

    plot_run_pico_data(pico_single_run_data, run_info)

    analyse_GPIO_run_data(gpio_single_run_data[0])

def analyse_all_runs(folder_path, angles):

    # analysing all runs - to be done at the end of all measurements (12 or 8 rotations per inlet condition)

    test_runs = create_dataclasses_for_run(folder_path, angles)

    processed_data = sort_test_runs(test_runs, angles)

    for i in range(len(test_runs)):

        analyse_GPIO_run_data(processed_data["GPIO_structs"][i])

        analyse_all_pico_data(processed_data)

def compare_requested_to_actual_transient_response(run_number: str, date):

    # only have GPIO data in "analysis/data/PIDTuning/actual"

    requested_folder = "analysis/data/PIDTuning/requested/" + date + "/"

    actual_folder = "analysis/data/PIDTuning/actual/" + date + "/"

    requested_folder_path = requested_folder + "run" + run_number

    actual_folder_path = actual_folder + "run" + run_number

    file_list = os.listdir(requested_folder_path)
    file_list.sort(key=lambda x: os.path.getctime(os.path.join(requested_folder_path, x)))

    print(f"Analysing: {file_list}")

    # Initialize empty arrays for 

    all_requested_runs = []

    for filename in file_list:

        requested_times = []

        requested_actuator_position = []

        if filename.endswith('.csv'):  # Filter CSV files
 
            file_path = os.path.join(requested_folder_path, filename)

            # Read CSV file and populate arrays
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    requested_times.append(float(row[0]))
                    requested_actuator_position.append(float(row[1]))

            all_requested_runs.append((requested_times, requested_actuator_position))
        
    experiments = process_individual_run(actual_folder_path) # experiments is a list of classes

    GPIO_run_data = []

    for experiment in experiments: 

        GPIO_run_data.append(extract_GPIO_data(experiment)) # GPIO_run_data is a list of dictionaries

    for index, run_data in enumerate(GPIO_run_data):

        if len(run_data["branch_flow_meter"][1]) != 0: 

            # then plot things, error next to actual and error 

            branch_times_data, branch_flow_rate_data, branch_filtered_flow_rate_data = run_data["branch_flow_meter"][0], run_data["branch_flow_meter"][1], exponential_filter(run_data["branch_flow_meter"][1])

            TB_motor_times_data, TB_motor_times_state, time_0_reference = run_data["TB_motor"][0], run_data["TB_motor"][1], run_data["time_0_reference"]

            PIV_signal_times_data, PIV_signal_times_state = run_data["PIV_signal"][0], run_data["PIV_signal"][1]

            time = run_data["time"]

            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,8))

            axes[0].set_xlabel('Time (s)')
            axes[0].set_ylabel('Flow Rate (ml/s)')
            axes[0].set_title('Requested and Actual Flow Rates')
            axes[0].legend(loc='best')

            # plotting actual and filtered flow rates

            sns.scatterplot(x=branch_times_data, y=branch_flow_rate_data, ax=axes[0], label="Branch Flow Rate Raw", s=5, color="red")

            sns.lineplot(x=branch_times_data, y=branch_filtered_flow_rate_data, ax=axes[0], label="Branch Flow Rate Filtered", color="blue")

            requested_times, requested_actuator_position = all_requested_runs[index]

            requested_actuator_position_interpolated = np.interp(branch_times_data, requested_times, requested_actuator_position)

            sns.lineplot(x=branch_times_data, y=requested_actuator_position_interpolated, ax=axes[0], label="Requested Actuator Movement", color="green", markers=True)

            axes[1].set_xlim(-1, max(branch_times_data) + 1)

            axes[1].set_xlabel('Time (s)')
            axes[1].set_ylabel('Error (ml/s)')
            axes[1].set_title('Branch Flow Rates and Signals')    
            axes[1].legend(loc='best')

            error = requested_actuator_position_interpolated - branch_filtered_flow_rate_data

            sns.lineplot(x=branch_times_data, y=error, ax=axes[1], label="Error", color="black")

            fig.canvas.manager.set_window_title('Figure 1') 
            fig.suptitle(f'Branch Flow Rates at Start Time: {time}')  
                                    
            plt.tight_layout()

            plt.show()

            # plotting fft for branch data

            #  branch_times_data, branch_flow_rate_data, branch_filtered_flow_rate_data


            max_dt = float('-inf')

            for i in range(1, len(branch_times_data)):
                diff = branch_times_data[i] - branch_times_data[i-1]
                if diff > max_dt:
                    max_dt = diff

            constant_dt = max_dt / 3 

            # Create a new set of time values with constant interval
            new_time = np.arange(branch_times_data[0], branch_times_data[-1], constant_dt)

            # Interpolate the data to the new time values
            new_data = np.interp(new_time, branch_times_data, branch_flow_rate_data)

            fft_filtered = np.abs(np.fft.fft(exponential_filter(new_data, alpha=0.1))[:len(new_data)//2])
            fft_unfiltered = np.abs(np.fft.fft(new_data)[:len(new_data)//2])

            PSD_filtered = constant_dt * (fft_filtered ** 2)
            PSD_unfiltered = constant_dt * (fft_unfiltered ** 2)

            freq = np.fft.fftfreq(new_time.shape[-1])[:len(new_data)//2]

            unfiltered_FRF = fft_filtered / fft_unfiltered

            FRF = unfiltered_FRF

            fig, axes = plt.subplots()

            plt.plot(freq, PSD_filtered, label="Filtered", linewidth=0.5)
            plt.plot(freq, PSD_unfiltered, label="Unfiltered", linewidth=0.5)

            axes.set_yscale('log')
            axes.set_xscale('log')
            plt.legend()
            plt.show()

            fig, axes = plt.subplots()
            plt.plot(freq, FRF, label="FRF")
            axes.set_yscale('log')
            axes.set_xscale('log')
            plt.show()

        if len(run_data["main_flow_meter"][1]) != 0:

            main_times_data, main_flow_rate_data, main_filtered_flow_rate_data = run_data["main_flow_meter"][0], run_data["main_flow_meter"][1], exponential_filter(run_data["main_flow_meter"][1])

            TB_motor_times_data, TB_motor_times_state = run_data["TB_motor"][0], run_data["TB_motor"][1]

            PIV_signal_times_data, PIV_signal_times_state = run_data["PIV_signal"][0], run_data["PIV_signal"][1]

            sns.scatterplot(x=main_times_data, y=main_flow_rate_data, label="Branch Flow Rate Raw", s=5, color="red")

            sns.lineplot(x=main_times_data, y=main_filtered_flow_rate_data, label="Branch Flow Rate Filtered", color="blue")

            plt.plot()



if __name__ == "__main__":

    # Looking at data for a particular inlet condition 

    orientations = [0, 30, 90, 120, 180, 210, 240, 270]  
    
    # folder_path = 'analysis/data/opaque/inlet1'

    # analyse_all_runs(folder_path, angles)

    temperature_condition = "60"
    orientation_number = "1"
    date = "31May"
    momentum_ratio = "2"
    pid_run_number = "6"

    run_folder_path = "analysis/data/opaque/" + date + "/" + "orientation" + orientation_number + "/" + "temp" + temperature_condition + "/" + "momentum" + momentum_ratio
    
    # analyse_single_run(run_folder_path, orientations[int(orientation_number)-1]) 

    compare_requested_to_actual_transient_response(pid_run_number, date)







