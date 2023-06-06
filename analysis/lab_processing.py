import os 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, scale

from data_structs import Datalogger_Data, GPIO_Data
from extracting_data import extract_GPIO_data, create_dataclasses_for_run, sort_test_runs, process_individual_run, extract_pico_data


def plot_run_pico_data(pico_single_run_data, orientation_string):

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

            axes[index].set_xlabel('Time (s)')
            axes[index].set_ylabel('Pressure (mV)')
            axes[index].set_title(f'PRESSURE - LOCATION: {data.location} at {data.rotation_angle} degrees')
            axes[index].set_ylim(-0.6, 0)

            temp_values, time_values_seconds = extract_pico_data(data)

            sns.scatterplot(x=time_values_seconds, y=temp_values, ax=axes[index], s=10)
    
        fig1.canvas.manager.set_window_title('PRESSURES') 
        
        fig1.suptitle(f'Pressures vs Time, {orientation_string}')

        fig1.subplots_adjust(wspace=0.3)

        plt.show()

    def plot_opaque_temperatures(opaque_temps):

        # plot temperatures as seperate plots 

        fig2, axes1 = plt.subplots(nrows=3, ncols=3, figsize=(15, 8))

        matrix = [opaque_temps[i:i+3] for i in range(0, 9, 3)]

        for i in range(len(matrix)):

            for j in range(len(matrix)):

                axes1[i][j].set_xlabel('Time (s)')

                axes1[i][j].set_ylabel('Temperature (Degrees)')
                axes1[i][j].set_ylim(20, 40)

                axes1[i][j].set_title(f'LOCATION: {matrix[i][j].location} at {matrix[i][j].depth} mm {matrix[i][j].rotation_angle} degrees')

                if matrix[i][j].location == '-69':

                    axes1[i][j].set_title(f'Cold Junction Compensation')

                temp_values, time_values_seconds = extract_pico_data(matrix[i][j])

                sns.scatterplot(x=time_values_seconds, y=temp_values, ax=axes1[i][j], s=5)
        
        fig2.canvas.manager.set_window_title('PICO LOGGER DATA') 
        fig2.suptitle(f'Temperature vs Time, at {orientation_string}')

        plt.subplots_adjust(hspace=0.5)

        plt.show()

        return {}

    def plot_testbed_temperatures(test_bed_temps):

        fig2, axes1 = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

        for index, data in enumerate(test_bed_temps):

            if data.unit == "UNIT2":

                if data.channel == "CHANNEL7": # Main Inlet

                    axes1[0].set_title(f'TEMP - MAIN INLET')

                    axes1[0].set_ylabel('Temperature (Degrees)')
                
                    axes1[0].set_ylim(10, 80)

                    temp_values, time_values_seconds = extract_pico_data(data)

                    sns.scatterplot(x=time_values_seconds, y=temp_values, ax=axes1[0], s=5)

                if data.channel == "CHANNEL8": # Branch Inlet

                    axes1[1].set_title(f'TEMP - BRANCH INLET')

                    axes1[1].set_ylabel('Temperature (Degrees)')
                
                    axes1[1].set_ylim(10, 80)

                    temp_values, time_values_seconds = extract_pico_data(data)

                    sns.scatterplot(x=time_values_seconds, y=temp_values, ax=axes1[1], s=5)

        fig2.canvas.manager.set_window_title('PICO LOGGER DATA') 
        fig2.suptitle(f'Temperature vs Time, at {orientation_string}')

        plt.subplots_adjust(hspace=0.5)

        plt.show()

        return {}

    def plot_transparent_temperatures(test_bed_temps):

            fig2, axes1 = plt.subplots(nrows=1, ncols=3, figsize=(12, 5))

            for index, data in enumerate(test_bed_temps):

                if data.unit == "UNIT2":

                    if data.channel == "CHANNEL3": # Transparent 1

                        axes1[0].set_title(f'TEMP - Transparent 1')

                        axes1[0].set_ylabel('Temperature (Degrees)')
                    
                        axes1[0].set_ylim(10, 80)

                        temp_values, time_values_seconds = extract_pico_data(data)

                        sns.scatterplot(x=time_values_seconds, y=temp_values, ax=axes1[0], s=5)

                    if data.channel == "CHANNEL4": # Transparent 2

                        axes1[1].set_title(f'TEMP - Transparent 2')

                        axes1[1].set_ylabel('Temperature (Degrees)')
                    
                        axes1[1].set_ylim(10, 80)

                        temp_values, time_values_seconds = extract_pico_data(data)

                        sns.scatterplot(x=time_values_seconds, y=temp_values, ax=axes1[1], s=5)
                    
                    if data.channel == "CHANNEL5": # Transparent 3

                        axes1[2].set_title(f'TEMP - Transparent 3')

                        axes1[2].set_ylabel('Temperature (Degrees)')
                    
                        axes1[2].set_ylim(10, 80)

                        temp_values, time_values_seconds = extract_pico_data(data)

                        sns.scatterplot(x=time_values_seconds, y=temp_values, ax=axes1[2], s=5)

    plot_pressures(pressures)
    plot_opaque_temperatures(opaque_temps)
    plot_testbed_temperatures(test_bed_temps)
    plot_transparent_temperatures(test_bed_temps)

def get_data_from_run_folder_path(run_folder_path, angle):

    data = {}

    file_list = os.listdir(run_folder_path)

    print(f"Analysing: {file_list}")

    experiment_data = process_individual_run(run_folder_path, angle)

    datalogger_classes = []
    gpio_classes = []

    for class_instance in experiment_data:
        if isinstance(class_instance, Datalogger_Data):
            datalogger_classes.append(class_instance)
        elif isinstance(class_instance, GPIO_Data):
            gpio_classes.append(class_instance)

    data["GPIO"] = gpio_classes
    data["Pico"] = datalogger_classes

    return data

def exponential_filter(x,alpha=0.05):

    s = np.zeros(len(x))

    s[0] = x[0]

    for t in range(1,len(x)):
        s[t] = alpha*x[t] + (1-alpha)*s[t-1]

    return s

def actual_transient_response_from_opaque(run_folder_path, angle): 

    gpio_data = get_data_from_run_folder_path(run_folder_path, angle)["GPIO"]

    momentum_ratio_string = run_folder_path.split("/")[-1].upper()

    GPIO_run_data = []

    for data in gpio_data: 

        GPIO_run_data.append(extract_GPIO_data(data)) # GPIO_run_data is a list of dictionaries

    for index, run_data in enumerate(GPIO_run_data):

        if len(run_data["branch_flow_meter"][1]) != 0: 

            # then plot things, error next to actual and error 

            branch_times_data, branch_flow_rate_data, branch_filtered_flow_rate_data = run_data["branch_flow_meter"][0], run_data["branch_flow_meter"][1], exponential_filter(run_data["branch_flow_meter"][1])

            TB_motor_times_data, TB_motor_times_state, time_0_reference = run_data["TB_motor"][0], run_data["TB_motor"][1], run_data["time_0_reference"]

            PIV_signal_times_data, PIV_signal_times_state = run_data["PIV_signal"][0], run_data["PIV_signal"][1]

            time = run_data["time"]

            fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15,8))

            axes.set_xlabel('Time (s)')
            axes.set_ylabel('Flow Rate (ml/s)')
            axes.set_title('Actual Flow Rates')
            axes.set_xlim(-1, max(branch_times_data) + 1)
            axes.legend(loc='best')
            # axes[0].set_ylim(20, 35)

            sns.scatterplot(x=branch_times_data, y=branch_flow_rate_data, ax=axes, label="Branch Flow Rate Raw", s=5, color="red")

            sns.lineplot(x=branch_times_data, y=branch_filtered_flow_rate_data, ax=axes, label="Branch Flow Rate Filtered", color="blue") 

            fig.canvas.manager.set_window_title('Figure 1') 
            fig.suptitle(f'Branch Flow Rates ({momentum_ratio_string}) at Start Time: {time}')  
                                    
            plt.tight_layout()

            plt.show()

            # max_dt = float('-inf')

            # for i in range(1, len(branch_times_data)):
            #     diff = branch_times_data[i] - branch_times_data[i-1]
            #     if diff > max_dt:
            #         max_dt = diff

            # constant_dt = max_dt / 3 

            # Create a new set of time values with constant interval
            # new_time = np.arange(branch_times_data[0], branch_times_data[-1], constant_dt)

            # Interpolate the data to the new time values
            # new_data = np.interp(new_time, branch_times_data, branch_flow_rate_data)

            # fft_filtered = np.abs(np.fft.fft(exponential_filter(new_data, alpha=0.01))[:len(new_data)//2])
            # fft_unfiltered = np.abs(np.fft.fft(new_data)[:len(new_data)//2])

            # PSD_filtered = constant_dt * (fft_filtered ** 2)
            # PSD_unfiltered = constant_dt * (fft_unfiltered ** 2)

            # freq = np.fft.fftfreq(new_time.shape[-1])[:len(new_data)//2]

            # unfiltered_FRF = fft_filtered / fft_unfiltered

            # FRF = unfiltered_FRF

            # fig, axes = plt.subplots()

            # plt.plot(freq, PSD_filtered, label="Filtered", linewidth=0.5)
            # plt.plot(freq, PSD_unfiltered, label="Unfiltered", linewidth=0.5)

            # plt.xlabel("Frequency (Hz)")
            # plt.ylabel("Power Spectral Density")

            # axes.set_yscale('log')
            # axes.set_xscale('log')
            # plt.title("Power Spectral Density Analysis")
            # plt.legend()
            # plt.show()

            # fig, axes = plt.subplots()
            # plt.plot(freq, 20*np.log10(FRF), label="FRF (dB)", color="blue", linewidth=0.1)
            # plt.plot(freq, exponential_filter(20*np.log10(FRF), alpha=0.01), color="red", label="FRF (dB) Averaged")
            # axes.set_xscale('log')
            # plt.xlabel("Frequency (Hz)")
            # plt.ylabel("Gain (dB)")
            # plt.title("Frequency Response Function")
            # plt.show()    

    return {}

def plot_transient_temperature(run_folder_path, angle):

    pico_data = get_data_from_run_folder_path(run_folder_path, angle)["Pico"]

    orientation_string = run_folder_path.split("/")[4].upper()

    plot_run_pico_data(pico_data,orientation_string)

    return {}

if __name__ == "__main__":

    orientation_angles = [0, 30, 90, 120, 180, 210, 240, 270]  # check powerpoint slide for definition of 0 degrees

    run_folder_path = "analysis/data/opaque/5Jun/orientation8/temp60/momentum3"

    orientation_index = int(run_folder_path.split("/")[4][-1]) - 1

    actual_transient_response_from_opaque(run_folder_path, orientation_angles[orientation_index]) 

    plot_transient_temperature(run_folder_path, orientation_angles[orientation_index])  


