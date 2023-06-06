import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random as rn
import scipy.stats as stats


from data_structs import Datalogger_Data, GPIO_Data
from extracting_data import extract_GPIO_data, create_dataclasses_for_run, sort_test_runs, process_individual_run, extract_pico_data

np.random.seed(1234)

def FlowRateChange(data,new_mean=500,new_var=50):

    # Calculate the mean and variance of the original count data
    data_mean = np.mean(data)
    data_var = np.var(data)

    # Calculate the scaling factor
    scaling_factor = np.sqrt(new_var / data_var)

    transform_factor = new_mean / data_mean

    data_new = []

    print(type(data))
    print(len(data))

    for i in range(len(data)):

        # Multiply the original count data by the scaling factor
        data_new_value = transform_factor + (data[i] * int(scaling_factor))
        data_new.append(data_new_value)

    # Calculate the new mean and variance of the transformed counts
    data_new_mean = np.mean(data_new)
    data_new_var = np.var(data_new)

    print("Original Mean:", data_mean)
    print("Original Variance:", data_var)
    print("Transformed Mean:", data_new_mean)
    print("Transformed Variance:", data_new_var)

    return data_new

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

            main_flow_rate_data = FlowRateChange(branch_flow_rate_data)

            print(type(branch_flow_rate_data))
            print(type(main_flow_rate_data))

            print(len(branch_flow_rate_data))
            print(len(main_flow_rate_data))
            print(len(branch_times_data))

            # Create an array to store the bootstrap temperature values
            bootstrapping_iter = 5
            for n in range(bootstrapping_iter):
                main_flow_rate_data_resampled = [] # Initialising the resampled data
                for i in range(len(main_flow_rate_data)): # Iterating through the length of the input data i.e. all the data
                    resample = np.random.choice(main_flow_rate_data, replace=True) + np.random.normal(0,5**2) # Producing and replacing a random new value given the input data
                    main_flow_rate_data_resampled.append(resample) # Adding this new value to resampled_data to then be returned
                    #resampled_data = np.percentile(resampled_data, [2.5, 97.5], axis=0)

            main_filtered_flow_rate_data = exponential_filter(main_flow_rate_data_resampled)

            fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15,8))

            axes.set_xlabel('Time (s)')
            axes.set_ylabel('Flow Rate (ml/s)')
            axes.set_title('Actual Flow Rates')
            axes.set_xlim(-1, max(branch_times_data) + 1)
            axes.legend(loc='best')
            # axes[0].set_ylim(20, 35)

            sns.scatterplot(x=branch_times_data, y=main_flow_rate_data_resampled, ax=axes, label="Main Flow Rate Raw", s=5, color="red")

            sns.lineplot(x=branch_times_data, y=main_filtered_flow_rate_data, ax=axes, label="Main Flow Rate Filtered", color="blue") 

            fig.canvas.manager.set_window_title('Figure 1') 
            fig.suptitle(f'Main Flow Rates ({momentum_ratio_string}) at Start Time: {time}')  
                                    
            plt.tight_layout()

            plt.show()

            branch_diameter = 12
            main_diamter = 38

            momentum_ratio = (4 * branch_diameter**(3) * main_filtered_flow_rate_data**(2)) / (np.pi * main_diamter**(3) * branch_filtered_flow_rate_data**(2))
            momentum_ratio_filtered = exponential_filter(momentum_ratio)

            fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15,8))

            axes.set_xlabel('Time (s)')
            axes.set_ylabel('Momentum Ratio')
            axes.set_title('Momentum Ratio against Time')
            axes.set_xlim(-1, max(branch_times_data) + 1)
            # axes[0].set_ylim(20, 35)

            sns.scatterplot(x=branch_times_data, y=momentum_ratio, ax=axes, label="Momentum Ratio", s=5, color="red")

            sns.lineplot(x=branch_times_data, y=momentum_ratio_filtered, ax=axes, label="Momentum Ratio Filtered", color="blue") 
            axes.axhline(np.mean(momentum_ratio_filtered), label='Momentum Ratio Mean Value',color='green',linewidth=2)

            fig.canvas.manager.set_window_title('Figure 1') 
            fig.suptitle(f'Momentum Ratio ({momentum_ratio_string}) at Start Time: {time}')  
                                    
            axes.legend(loc='best')

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


def exponential_filter(x,alpha=0.05):

    print(len(x))

    s = np.zeros(len(x))

    s[0] = x[0]

    for t in range(1,len(x)):
        s[t] = alpha*x[t] + (1-alpha)*s[t-1]

    return s

if __name__ == "__main__":

    orientation_angles = [0, 30, 90, 120, 180, 210, 240, 270]  # check powerpoint slide for definition of 0 degrees

    run_folder_path = "analysis/data/opaque/5Jun/orientation7/temp60/momentum3"

    orientation_index = int(run_folder_path.split("/")[4][-1]) - 1

    actual_transient_response_from_opaque(run_folder_path, orientation_angles[orientation_index]) 

    #plot_transient_temperature(run_folder_path, orientation_angles[orientation_index])  

# data = pd.read_csv('c:/Users/jimty/Documents/University/Coursework/M03_DMT/DMT16_DAQ/analysis/data/opaque/5Jun/orientation4/temp60/momentum3/UNIT2-2023_06_05_17_43_36-CHANNEL2-temp.csv', header=0) # NOTE: Local location of .csv file

# plt.rcParams["figure.figsize"] = [18,9.5] # Forming the Size of the Plot (and all future plots)

# # Extract the data from the columns using the heading title names for the .csv read
# temperature_data = data['temp_buffers'].to_numpy() # x represents the time index
# time_data = data['times_ms_buffers'].to_numpy() # y represents the wavelength, measured in nanometres.
# date_data = data['Time'].to_numpy()

# plt.scatter(time_data, temperature_data, label='Raw')

# # Assuming you have your original temperature values stored in a NumPy array called 'temperature_data'
# mean = np.mean(temperature_data)
# print('mean:', mean)
# residuals = temperature_data - mean
# variance = np.var(residuals)
# print('var:', variance)

# plt.axhline(mean)

# # Set the number of bootstrap samples you want to generate
# num_bootstraps = 1000

# # Create an array to store the bootstrap temperature values
# bootstrap_temperatures = np.empty_like(temperature_data)
# bootstrapping_iter = 100
# for n in range(bootstrapping_iter):
#     resampled_data = [] # Initialising the resampled data
#     for i in range(len(temperature_data)): # Iterating through the length of the input data i.e. all the data
#         resample = np.random.normal(0,0.01)*np.random.choice(temperature_data, replace=True) - 0.12 # Producing and replacing a random new value given the input data
#         resampled_data.append(resample) # Adding this new value to resampled_data to then be returned

# plt.scatter(time_data, resampled_data, label='Bootstrap')

# plt.axhline(np.mean(resampled_data), color='orange')

# plt.legend()

# plt.show()

# print('mean', np.mean(resampled_data))
# print('var', np.var(resampled_data))

# data_new = [resampled_data,time_data,date_data]
# for row in data_new:
#     for item in row:
#         print(item)