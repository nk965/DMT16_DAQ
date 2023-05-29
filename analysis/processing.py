import os 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_structs import Datalogger_Data, GPIO_Data
from channel_info import channel_info, null

from extracting_data import extract_GPIO_data, create_dataclasses_for_run, sort_test_runs

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

def analyse_all_runs(folder_path, angles):

    # analysing all runs - to be done at the end of all measurements (12 or 8 rotations per inlet condition)

    test_runs = create_dataclasses_for_run(folder_path, angles)

    processed_data = sort_test_runs(test_runs, angles)

    for i in range(len(test_runs)):

        # analyse_GPIO_run_data(processed_data["GPIO_structs"][i])

        analyse_all_pico_data(processed_data)

    return {}

def analyse_single_run():

    # on the spot running of data

    # analyse_GPIO_run_data(processed_data["GPIO_structs"]) i.e., not indexed in comparison to use in "analyse_all_runs"

    return {}

if __name__ == "__main__":

    # Looking at data for a particular inlet condition 

    angles = [0, 30, 60]  
    
    folder_path = 'analysis/data/opaque/inlet1'

    analyse_all_runs(folder_path, angles)
    
    analyse_single_run()






