import os 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

from extracting_data import extract_GPIO_data, create_dataclasses_for_run, sort_test_runs, process_individual_run, extract_pico_data

sns.set_theme()

def exponential_filter(x,alpha=0.3):

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

def plot_run_pico_data(pico_single_run_data):

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
        
        fig1.canvas.manager.set_window_title('Figure 1') 
        
        fig1.suptitle(f'Figure 1: Pressures vs Time')
        
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
        
        fig2.canvas.manager.set_window_title('Figure 1') 
        
        fig2.suptitle(f'Figure 1: Temperatures vs Time')

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
        
        fig3.canvas.manager.set_window_title('Figure 1') 
        
        fig3.suptitle(f'Figure 1: Temperatures vs Time')

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

    plot_run_pico_data(pico_single_run_data)

    analyse_GPIO_run_data(gpio_single_run_data[0])

def analyse_all_runs(folder_path, angles):

    # analysing all runs - to be done at the end of all measurements (12 or 8 rotations per inlet condition)

    test_runs = create_dataclasses_for_run(folder_path, angles)

    processed_data = sort_test_runs(test_runs, angles)

    for i in range(len(test_runs)):

        analyse_GPIO_run_data(processed_data["GPIO_structs"][i])

        analyse_all_pico_data(processed_data)

def compare_requested_to_actual_response(requested_folder_path, actual_folder_path):

    # only have GPIO data in "analysis/data/PIDTuning/actual"

    experiments = process_individual_run(actual_folder_path)

    GPIO_run_data = extract_GPIO_data(experiments[0]) # edit the index 

    filtered_branch = exponential_filter(GPIO_run_data["branch_flow_meter"][1])

    fig1, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8)) 
    axes[0].set_xlabel('Time (s)')
    axes[0].set_ylabel('Flow Rate (ml/s)')
    axes[0].set_title(f'Branch Flow Rates at Start Time: {experiments[0].start_time}') # Index
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel('Flow Rate (ml/s)')
    axes[1].set_title('Main Flow Rates and Signals')    
    
    axes[0].legend(loc='best')
    axes[1].legend(loc='best')
    
    fig1.canvas.manager.set_window_title('Figure 1') 
    fig1.suptitle('Actual Flow Rates')   

    sns.scatterplot(x=GPIO_run_data["branch_flow_meter"][0], y=GPIO_run_data["branch_flow_meter"][1], ax=axes[0], label="Branch Flow Rate Raw", s=5, color="red")  

    sns.scatterplot(x=GPIO_run_data["main_flow_meter"][0], y=GPIO_run_data["main_flow_meter"][1], ax=axes[1], label="Main Flow Rate Raw", s=5)
     
    # sns.lineplot(x=GPIO_run_data["main_flow_meter"][0], y=filtered_main, ax=axes, label="Main Flow Rate Filtered")  

    sns.lineplot(x=GPIO_run_data["branch_flow_meter"][0], y=filtered_branch, ax=axes[0], label="Branch Flow Rate Filtered")      
                
    plt.tight_layout()

    plt.show()

    # Initialize empty arrays for 
    requested_times = []
    requested_actuator_position = []

    for filename in os.listdir(requested_folder_path):

        if filename.endswith('.csv'):  # Filter CSV files
 
            file_path = os.path.join(requested_folder_path, filename)

            # Read CSV file and populate arrays
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    requested_times.append(float(row[0]))
                    requested_actuator_position.append(float(row[1]))

    # Interpolation

    requested_actuator_position_interpolated = np.interp(GPIO_run_data["branch_flow_meter"][0], requested_times, requested_actuator_position)

    error = filtered_branch - requested_actuator_position_interpolated

    sns.lineplot(x=GPIO_run_data["branch_flow_meter"][0], y=GPIO_run_data["branch_flow_meter"][1], label='Actual')
    sns.scatterplot(x=requested_times, y=requested_actuator_position, color='red', label='Requested')
    plt.legend()

    plt.show()    

    # fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    # axes[0].set_xlabel('Time (s)')
    # axes[0].set_ylabel('Flow Rate')
    # axes[0].set_title('Flow Rate vs Time, Requested and Actual') 

    # sns.lineplot(x=GPIO_run_data["branch_flow_meter"][0], y=GPIO_run_data["branch_flow_meter"][1], label='Actual', ax=axes[0])
    # sns.scatterplot(x=requested_times, y=requested_actuator_position, color='red', label='Requested', ax=axes[0])

    # axes[1].set_xlabel('Time (s)')
    # axes[1].set_ylabel('Flow Rate')
    # axes[1].set_title('Error')

    # # sns.lineplot(x=GPIO_run_data["branch_flow_meter"][0], y=error, label='Requested', linewidth=0.45, ax=axes[1])

    # fig.canvas.manager.set_window_title('Figure 5') 
    # fig.suptitle(f'PID Closed Loop Flow Actuator Control Plots')
    # fig.subplots_adjust(wspace=0.5)

    # plt.tight_layout

    # plt.show()

    # for index, experiment in enumerate(experiments): 
    #     GPIO_run_data = extract_GPIO_data()



if __name__ == "__main__":

    # Looking at data for a particular inlet condition 

    angles = [0, 30, 60]  
    
    # folder_path = 'analysis/data/opaque/inlet1'

    # analyse_all_runs(folder_path, angles)

    # run_folder_path = "analysis/data/opaque/inlet1/run2"
    
    # analyse_single_run(run_folder_path, angles[0]) 

    requested_folder_path = "analysis/data/PIDTuning/requested/run6"

    actual_folder_path = "analysis/data/PIDTuning/actual/run6"

    compare_requested_to_actual_response(requested_folder_path, actual_folder_path)







