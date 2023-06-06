import os 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, scale
import scipy.stats as sci_stats

from data_structs import Datalogger_Data, GPIO_Data
from extracting_data import extract_GPIO_data, create_dataclasses_for_run, sort_test_runs, process_individual_run, extract_pico_data

sns.set_theme()

symmetry_and_extremes_map = {
    "one_mm": {
        "symmetry": ("orientation1", "orientation5"),
        "extremes": ("orientation3", "orientation7"),
    },
    "four_mm": {
        "symmetry": ("orientation3", "orientation7"),
        "extremes": ("orientation1", "orientation5"),
    },
    "pressures": {
        "symmetry": ("orientation2", "orientation6"),
        "extremes": ("orientation4", "orientation8"),
    }, 
}

def find_time_0(dataclass):

    class_specific_file_path = dataclass.file_path

    parent_directory = "/".join(class_specific_file_path.split("/")[:-1])

    print(dataclass.print_status())

    for filename in os.listdir(parent_directory):

        if filename.endswith('.csv'):  # Filter CSV files
 
            file_path = os.path.join(parent_directory, filename)

            filename_array = filename.split("-")

            if filename_array[0] == 'RPI':
                
                GPIO_data = GPIO_Data(file_path)

    time_0_reference = extract_GPIO_data(GPIO_data)["time_0_reference"]

    return time_0_reference

def pressure_scaling(data):
    data_new = data*-10
    return data_new


def create_dataclasses_for_all_orientations(run_folder_path, momentum_ratio_string, temp_string, angles):

    test_runs = []

    # process_individual_run on the level of momentum3

    # Get a list of directory names in the run folder
    directories = [entry.name for entry in os.scandir(run_folder_path) if entry.is_dir() and entry.name != '.DS_Store']

    # Sort the directory names in alphabetical order
    sorted_directories = sorted(directories)

    # Process each directory in the sorted order
    for index, directory_name in enumerate(sorted_directories):
        
        orientation_folder = os.path.join(run_folder_path, directory_name)
        
        print(f'Processing data in: {orientation_folder}')

        subfolder_path = os.path.join(orientation_folder, temp_string, momentum_ratio_string)
        
        # append all classes in a list called test_runs 

        test_runs.append(process_individual_run(subfolder_path, angles[index]))

    return test_runs 

def analyse_all_runs(folder_path, momentum_ratio_string, temp_string, angles):

    # analysing all runs - to be done at the end of all measurements (12 or 8 rotations per inlet condition)

    test_runs = create_dataclasses_for_all_orientations(folder_path, momentum_ratio_string, temp_string, angles)

    processed_data = sort_test_runs(test_runs, angles)

    for data in processed_data["pressures"]:

        data.print_status()

    # sorted_structs = {"pressures": pressures, "test_bed_temps": test_bed_temps, "four_mm": four_mm, "three_mm": three_mm, "two_mm": two_mm, "one_mm": one_mm, "GPIO_structs": GPIO_structs}

    def get_temperature_rms_and_time_average(temperatures):

        temperature_depths = {"four_mm": {}, "three_mm": {}, "two_mm": {}, "one_mm": {}}
        
        for depths in temperature_depths:

            rms_array_left = []
            rms_array_right = []
            
            mean_left = []
            mean_right = []

            angular_displacement_left = []
            angular_displacement_right = []

            for data in temperatures[depths]:

                temp_values, time_values_seconds = extract_pico_data(data)

                squares = np.square(temp_values)  # Square each temperature
                mean = np.mean(squares)  # Calculate the mean of the squared temperatures

                if data.location == "Right":

                    rms_array_right.append(np.sqrt(mean))  # Take the square root of the mean

                    angular_displacement_left.append(data.rotation_angle)

                    mean_left.append(mean)

                if data.location == "Left":
                    
                    rms_array_left.append(np.sqrt(mean))  # Take the square root of the mean

                    angular_displacement_right.append(data.rotation_angle)
                    
                    mean_right.append(mean)

            temperature_depths[depths] = {"rms_array_left": rms_array_left, "rms_array_right": rms_array_right, "mean_left": mean_left, "mean_right": mean_right, "angular_displacement_right": angular_displacement_right, "angular_displacement_left": angular_displacement_left}

            fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
            # fig, ax = plt.subplots()

            angular_displacement_left = np.asarray(angular_displacement_left) * np.pi / 180
            angular_displacement_right = np.asarray(angular_displacement_right) * np.pi / 180        

            ax.scatter(angular_displacement_left, rms_array_left, label=f"{depths}, left")
            ax.scatter(angular_displacement_right, rms_array_right, label=f"{depths}, right")
            ax.set_xlabel("Angular Displacement")
            ax.set_xticks(np.arange(0, 2*np.pi, np.pi/6))
            ax.set_ylim(20, 35)
            ax.set_ylabel("Temperature RMS or Mean")
            ax.set_theta_direction(-1)
            ax.set_theta_zero_location("N")
            ax.legend()
            plt.show()
        
        return temperature_depths

    def get_pressure_rms_and_time_average(pressures):

        pressure_rms_time_average = {"left": {}, "right": {}}

        angular_displacement_left = []
        angular_displacement_right = []

        rms_array_right = []
        rms_array_left = []

        mean_left = []
        mean_right = []

        for data in pressures["pressures"]:

            temp_values, time_values_seconds = extract_pico_data(data)

            squares = np.square(temp_values)  # Square each pressure
            mean = np.mean(squares)  # Calculate the mean of the squared pressure

            if data.location == "Right": 

                angular_displacement_right.append(data.rotation_angle)

                rms_array_right.append(np.sqrt(mean))
                
                mean_right.append(mean)

            if data.location == "Left":

                angular_displacement_left.append(data.rotation_angle)

                rms_array_left.append(np.sqrt(mean))
                
                mean_left.append(mean)
        
        pressure_rms_time_average["left"] = {"rms_array_left": rms_array_left, "mean_left": mean_left, "angular_displacement_left": angular_displacement_left}

        pressure_rms_time_average["right"] = {"rms_array_right": rms_array_right, "mean_left": mean_right, "angular_displacement_left": angular_displacement_right}
        
        return pressure_rms_time_average
    
    
    temp_mean_and_rms_data = get_temperature_rms_and_time_average(processed_data)

    # pressure_mean_and_rms_data = get_pressure_rms_and_time_average(processed_data)

    # for i in range(len(test_runs)):

    #     # analyse_GPIO_run_data(processed_data["GPIO_structs"][i])

    #     analyse_all_pico_data(processed_data)

def analyse_temperatures_sym_and_extremes(run_folder_path, momentum_ratio_string, temp_string, orientation_angles, depth):

    def show_symmetry(run_folder_path, momentum_ratio_string, temp_string, angles, depth):

        orientation_sym1, orientation_sym2 = symmetry_and_extremes_map[depth]["symmetry"]

        orientation_no_1 = orientation_sym1[-1]
        orientation_no_2 = orientation_sym2[-1]

        angle_index_1 = int(orientation_no_1) - 1
        angle_index_2 = int(orientation_no_2) - 1

        orientation_folder1 = os.path.join(run_folder_path, orientation_sym1)
        orientation_folder2 = os.path.join(run_folder_path, orientation_sym2)

        subfolder_path1 = os.path.join(orientation_folder1, temp_string, momentum_ratio_string)
        subfolder_path2 = os.path.join(orientation_folder2, temp_string, momentum_ratio_string)

        test_run_1 = process_individual_run(subfolder_path1, angles[angle_index_1])
        test_run_2 = process_individual_run(subfolder_path2, angles[angle_index_2])

        depth_dictionary = {"one_mm": 1, "two_mm": 2, "three_mm": 3, "four_mm": 4}

        sym1_time_series = {}

        sym2_time_series = {}

        for data in test_run_1: 

            if data.type == "temp":

                if data.location == "Left":

                    if data.depth == depth_dictionary[depth]:

                        sym1_time_series["values_left"], sym1_time_series["time_values_left"] = extract_pico_data(data) 
                        
                        sym1_time_series["time_0_reference_left"] = find_time_0(data)

                if data.location == "Right":

                    if data.depth == depth_dictionary[depth]: 

                        sym1_time_series["values_right"], sym1_time_series["time_values_right"] = extract_pico_data(data)

                        sym1_time_series["time_0_reference_right"] = find_time_0(data)

        for data in test_run_2: 

            if data.type == "temp":

                if data.location == "Left":

                    if data.depth == depth_dictionary[depth]:

                        sym2_time_series["values_left"], sym2_time_series["time_values_left"] = extract_pico_data(data)
                        
                        sym2_time_series["time_0_reference_left"] = find_time_0(data)

                if data.location == "Right":

                    if data.depth == depth_dictionary[depth]: 

                        sym2_time_series["values_right"], sym2_time_series["time_values_right"] = extract_pico_data(data)

                        sym2_time_series["time_0_reference_right"] = find_time_0(data)

        return sym1_time_series, sym2_time_series

    def show_extremes(run_folder_path, momentum_ratio_string, temp_string, angles, depth):

        orientation_ext1, orientation_ext2 = symmetry_and_extremes_map[depth]["extremes"]

        orientation_no_1 = orientation_ext1[-1]
        orientation_no_2 = orientation_ext2[-1]

        angle_index_1 = int(orientation_no_1) - 1
        angle_index_2 = int(orientation_no_2) - 1

        orientation_folder1 = os.path.join(run_folder_path, orientation_ext1)
        orientation_folder2 = os.path.join(run_folder_path, orientation_ext2)

        subfolder_path1 = os.path.join(orientation_folder1, temp_string, momentum_ratio_string)
        subfolder_path2 = os.path.join(orientation_folder2, temp_string, momentum_ratio_string)

        test_run_1 = process_individual_run(subfolder_path1, angles[angle_index_1])
        test_run_2 = process_individual_run(subfolder_path2, angles[angle_index_2])

        depth_dictionary = {"one_mm": 1, "two_mm": 2, "three_mm": 3, "four_mm": 4}

        ext1_time_series = {}

        ext2_time_series = {}

        for data in test_run_1: 

            if data.type == "temp":

                if data.location == "Left":

                    if data.depth == depth_dictionary[depth]:

                        ext1_time_series["values_left"], ext1_time_series["time_values_left"] = extract_pico_data(data) 

                        ext1_time_series["time_0_reference_left"] = find_time_0(data)


                if data.location == "Right":

                    if data.depth == depth_dictionary[depth]: 

                        ext1_time_series["values_right"], ext1_time_series["time_values_right"] = extract_pico_data(data)

                        ext1_time_series["time_0_reference_right"] = find_time_0(data)

        for data in test_run_2:

            if data.type == "temp":

                if data.location == "Left":

                    if data.depth == depth_dictionary[depth]:

                        ext2_time_series["values_left"], ext2_time_series["time_values_left"] = extract_pico_data(data) 

                        ext2_time_series["time_0_reference_left"] = find_time_0(data)

                if data.location == "Right":

                    if data.depth == depth_dictionary[depth]: 

                        ext2_time_series["values_right"], ext2_time_series["time_values_right"] = extract_pico_data(data)

                        ext2_time_series["time_0_reference_right"] = find_time_0(data)

        return ext1_time_series, ext2_time_series

    extreme_temp_top, extreme_temp_bottom = show_extremes(run_folder_path, momentum_ratio_string, temp_string, orientation_angles, depth)
    
    symmetry_temp_west, symmetry_temp_east = show_symmetry(run_folder_path, momentum_ratio_string, temp_string, orientation_angles, depth)    

    # fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    # axes[0].set_xlabel("Time (s)")
    # axes[0].set_ylabel("Temperature Degrees")
    # axes[0].set_title("Axial Position Left")

    # axes[0].set_ylim(20, 40)    

    # sns.scatterplot(x=(sym1_time_series["time_values_left"] - sym1_time_series["time_0_reference_left"]), y=sym1_time_series["values_left"], ax=axes[0], label=angles[angle_index_1],s=10)
    # sns.scatterplot(x=(sym2_time_series["time_values_left"] - sym2_time_series["time_0_reference_left"]), y=sym2_time_series["values_left"], ax=axes[0], label=angles[angle_index_2],s=10)

    # axes[1].set_xlabel("Time (s)")
    # axes[1].set_ylabel("Temperature Degrees")
    # axes[1].set_title("Axial Position Right")

    # axes[1].set_ylim(20, 40)

    # sns.scatterplot(x=(sym1_time_series["time_values_right"] - sym1_time_series["time_0_reference_right"]), y=sym1_time_series["values_right"], ax=axes[1], label=angles[angle_index_1], s=10)
    # sns.scatterplot(x=(sym2_time_series["time_values_right"] - sym2_time_series["time_0_reference_right"]), y=sym2_time_series["values_right"], ax=axes[1], label=angles[angle_index_2], s=10)

    # fig.suptitle(f"Symmetry Analysis - {depth}")

    # plt.tight_layout()

    # plt.show()

    # fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    # axes[0].set_xlabel("Time (s)")
    # axes[0].set_ylabel("Temperature Degrees")
    # axes[0].set_title("Axial Position Left")

    # axes[0].set_ylim(20, 40)    

    # sns.scatterplot(x=(ext1_time_series["time_values_left"] - ext1_time_series["time_0_reference_left"]), y=ext1_time_series["values_left"], ax=axes[0], label=angles[angle_index_1],s=10)
    # sns.scatterplot(x=(ext2_time_series["time_values_left"] - ext2_time_series["time_0_reference_left"]), y=ext2_time_series["values_left"], ax=axes[0], label=angles[angle_index_2],s=10)

    # axes[1].set_xlabel("Time (s)")
    # axes[1].set_ylabel("Temperature Degrees")
    # axes[1].set_title("Axial Position Right")

    # axes[1].set_ylim(20, 40)

    # sns.scatterplot(x=(ext1_time_series["time_values_right"] - ext1_time_series["time_0_reference_right"]), y=ext1_time_series["values_right"], ax=axes[1], label=angles[angle_index_1], s=10)
    # sns.scatterplot(x=(ext2_time_series["time_values_right"] - ext2_time_series["time_0_reference_right"]), y=ext2_time_series["values_right"], ax=axes[1], label=angles[angle_index_2], s=10)

    # fig.suptitle(f"Extremes Analysis - {depth}")

    # plt.tight_layout()

    # plt.show()

def bootstrap_residuals(data):
    resampled_data = [] # Initialising the resampled data
    for i in range(len(data)): # Iterating through the length of the input data i.e. all the data
        resample = np.random.choice(data, replace=True) # Producing and replacing a random new value given the input data
        resampled_data.append(resample) # Adding this new value to resampled_data to then be returned
    return resampled_data # Function returns the resampled data following the random selection and replacement of the data.

def find_confidence_bands(values, model, bootstrap_int=1000):

    lower_band = []
    upper_band = []

    std_values = np.std(values)
    root_n = np.sqrt(len(values))

    values_new = []

    for i in range(bootstrap_int):

        residuals = values - model

        resample_residuals = bootstrap_residuals(residuals)

        values_new.append(model + resample_residuals)

    boot_quantiles = np.percentile(values_new, [2.5, 97.5], axis=0)

    lower_band = boot_quantiles[0]
    upper_band = boot_quantiles[1]

    return lower_band, upper_band

def analyse_pressures(run_folder_path, momentum_ratio_string, temp_string, angles): 

    def show_extremes_pres(run_folder_path, momentum_ratio_string, temp_string, angles):

        orientation_ext1, orientation_ext2 = symmetry_and_extremes_map["pressures"]["extremes"]

        orientation_no_1 = orientation_ext1[-1]
        orientation_no_2 = orientation_ext2[-1]

        angle_index_1 = int(orientation_no_1) - 1
        angle_index_2 = int(orientation_no_2) - 1

        orientation_folder1 = os.path.join(run_folder_path, orientation_ext1)
        orientation_folder2 = os.path.join(run_folder_path, orientation_ext2)

        subfolder_path1 = os.path.join(orientation_folder1, temp_string, momentum_ratio_string)
        subfolder_path2 = os.path.join(orientation_folder2, temp_string, momentum_ratio_string)

        test_run_1 = process_individual_run(subfolder_path1, angles[angle_index_1])
        test_run_2 = process_individual_run(subfolder_path2, angles[angle_index_2])

        ext1_time_series = {}

        ext2_time_series = {}

        for data in test_run_1:

            data.print_status()

            if data.type == "temp":

                if data.unit == "UNIT2":

                    if data.channel == "CHANNEL1":

                        ext1_time_series["values_left"], ext1_time_series["time_values_left"] = extract_pico_data(data)

                        # ext1_time_series["values_left"] = pressure_scaling(ext1_time_series["values_left"])

                        ext1_time_series["time_0_reference_left"] = find_time_0(data)

                    if data.channel == "CHANNEL2":

                        ext1_time_series["values_right"], ext1_time_series["time_values_right"] = extract_pico_data(data)

                        # ext1_time_series["values_right"] = pressure_scaling(ext1_time_series["values_right"])

                        ext1_time_series["time_0_reference_right"] = find_time_0(data)

        for data in test_run_2:

            if data.type == "temp":

                if data.unit == "UNIT2":

                    if data.channel == "CHANNEL1":

                        ext2_time_series["values_left"], ext2_time_series["time_values_left"] = extract_pico_data(data)

                        # ext2_time_series["values_left"] = pressure_scaling(ext2_time_series["values_left"])

                        ext2_time_series["time_0_reference_left"] = find_time_0(data)

                    if data.channel == "CHANNEL2":

                        ext2_time_series["values_right"], ext2_time_series["time_values_right"] = extract_pico_data(data)

                        # ext2_time_series["values_right"] = pressure_scaling(ext2_time_series["values_right"])

                        ext2_time_series["time_0_reference_right"] = find_time_0(data)

        return ext1_time_series, ext2_time_series

    def show_symmetry_pres(run_folder_path, momentum_ratio_string, temp_string, angles):

        orientation_sym1, orientation_sym2 = symmetry_and_extremes_map["pressures"]["symmetry"]

        orientation_no_1 = orientation_sym1[-1]
        orientation_no_2 = orientation_sym2[-1]

        angle_index_1 = int(orientation_no_1) - 1
        angle_index_2 = int(orientation_no_2) - 1

        orientation_folder1 = os.path.join(run_folder_path, orientation_sym1)
        orientation_folder2 = os.path.join(run_folder_path, orientation_sym2)

        subfolder_path1 = os.path.join(orientation_folder1, temp_string, momentum_ratio_string)
        subfolder_path2 = os.path.join(orientation_folder2, temp_string, momentum_ratio_string)

        test_run_1 = process_individual_run(subfolder_path1, angles[angle_index_1])
        test_run_2 = process_individual_run(subfolder_path2, angles[angle_index_2])

        sym1_time_series = {}

        sym2_time_series = {}

        for data in test_run_1: 
        
            if data.type == "temp":

                if data.unit == "UNIT2":

                    if data.channel == "CHANNEL1":

                        sym1_time_series["values_left"], sym1_time_series["time_values_left"] = extract_pico_data(data)

                        sym1_time_series["time_0_reference_left"] = find_time_0(data)

                    if data.channel == "CHANNEL2":

                        sym1_time_series["values_right"], sym1_time_series["time_values_right"] = extract_pico_data(data)

                        sym1_time_series["time_0_reference_right"] = find_time_0(data)

        for data in test_run_2:

            if data.type == "temp":

                if data.unit == "UNIT2":

                    if data.channel == "CHANNEL1":

                        sym2_time_series["values_left"], sym2_time_series["time_values_left"] = extract_pico_data(data)

                        sym2_time_series["time_0_reference_left"] = find_time_0(data)

                    if data.channel == "CHANNEL2":

                        sym2_time_series["values_right"], sym2_time_series["time_values_right"] = extract_pico_data(data)

                        sym2_time_series["time_0_reference_right"] = find_time_0(data)

        return sym1_time_series, sym2_time_series

    extremes_pressure_top, extremes_pressure_bottom = show_extremes_pres(run_folder_path, momentum_ratio_string, temp_string, angles)

    symmetry_pressure_west, symmetry_pressure_east = show_symmetry_pres(run_folder_path, momentum_ratio_string, temp_string, angles)

    fig1, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 8))

    # plt.errorbar(, y, yerr=y_err, xerr=x_err, ls='none', capsize=2, capthick=0.15, color='black', linewidth = 0.15)

    # Error calculation
    instrument_error = 3 / 100  # Convert percentage to decimal

    for i in range(len(axes)):

            axes[i].set_xlabel("Time (s)")
            axes[i].set_ylabel("Pressure (mV)") 
            axes[i].set_ylim(-0.6, 0)

    sns.scatterplot(x=(extremes_pressure_top['time_values_left'] - extremes_pressure_top['time_0_reference_left']), y=(extremes_pressure_top['values_left']), ax=axes[0], label="Top - 0°", s=10, color='#1f77b4')

    axes[0].errorbar((extremes_pressure_top['time_values_left'] - extremes_pressure_top['time_0_reference_left']), extremes_pressure_top['values_left'], yerr=abs(extremes_pressure_top['values_left']*instrument_error), ls='none', capsize=2, capthick=0.15, color='black', alpha=0.5, linewidth = 0.15)

    model_extreme_upstream_top = np.full(len(extremes_pressure_top['values_left']), np.mean(extremes_pressure_top['values_left']))

    lower_band_upstream_top, upper_band_upstream_top = find_confidence_bands(extremes_pressure_top['values_left'], model_extreme_upstream_top)

    sns.scatterplot(x=(extremes_pressure_bottom['time_values_left'] - extremes_pressure_bottom['time_0_reference_left']), y=(extremes_pressure_bottom['values_left']), ax=axes[0], label="Bottom - 180°", color="#2ca02c", s=10)

    axes[0].errorbar((extremes_pressure_bottom['time_values_left'] - extremes_pressure_bottom['time_0_reference_left']), extremes_pressure_bottom['values_left'], yerr=abs(extremes_pressure_bottom['values_left']*instrument_error), ls='none', capsize=2, capthick=0.15, alpha=0.5, color='black', linewidth = 0.15)

    model_extreme_upstream_bottom = np.full(len(extremes_pressure_bottom['values_left']), np.mean(extremes_pressure_bottom['values_left']))

    lower_band_upstream_bottom, upper_band_upstream_bottom = find_confidence_bands(extremes_pressure_bottom['values_left'], model_extreme_upstream_bottom)
    
    axes[0].fill_between(extremes_pressure_top['time_values_left'] - extremes_pressure_top['time_0_reference_left'] , lower_band_upstream_top, upper_band_upstream_top, alpha=0.3, color='#aec7e8') 

    axes[0].fill_between(extremes_pressure_bottom['time_values_left'] - extremes_pressure_bottom['time_0_reference_left'] , lower_band_upstream_bottom, upper_band_upstream_bottom, alpha=0.3, color="#98df8a") 

    axes[0].set_title("Upstream Pressure Readings")

    sns.scatterplot(x=(extremes_pressure_top['time_values_right'] - extremes_pressure_top['time_0_reference_right']), y=(extremes_pressure_top['values_right']), ax=axes[1], label="Top - 0°", color="#d62728", s=10)

    axes[1].errorbar((extremes_pressure_top['time_values_right'] - extremes_pressure_top['time_0_reference_right']), extremes_pressure_top['values_right'], yerr=abs(extremes_pressure_top['values_right']*instrument_error), ls='none', capsize=2, capthick=0.15, color='black', alpha=0.5, linewidth = 0.15)

    model_extreme_downstream_top = np.full(len(extremes_pressure_top['values_right']), np.mean(extremes_pressure_top['values_right']))

    lower_band_downstream_top, upper_band_downstream_top = find_confidence_bands(extremes_pressure_top['values_right'], model_extreme_downstream_top)

    axes[1].fill_between((extremes_pressure_top['time_values_right'] - extremes_pressure_top['time_0_reference_right']), lower_band_downstream_top, upper_band_downstream_top, alpha=0.3, color="#ff9896")
    
    sns.scatterplot(x=(extremes_pressure_bottom['time_values_right'] - extremes_pressure_bottom['time_0_reference_right']), y=(extremes_pressure_bottom['values_right']), ax=axes[1], label="Bottom - 180°", color="#9467bd", s=10)

    axes[1].errorbar((extremes_pressure_bottom['time_values_right'] - extremes_pressure_bottom['time_0_reference_right']), extremes_pressure_bottom['values_right'], yerr=abs(extremes_pressure_bottom['values_right']*instrument_error), ls='none', capsize=2, capthick=0.15, alpha=0.5, color='black', linewidth = 0.15)

    model_extreme_downstream_bottom = np.full(len(extremes_pressure_bottom['values_right']), np.mean(extremes_pressure_bottom['values_right']))

    lower_band_downstream_bottom, upper_band_downstream_bottom = find_confidence_bands(extremes_pressure_bottom['values_right'], model_extreme_downstream_bottom)

    axes[1].fill_between((extremes_pressure_bottom['time_values_right'] - extremes_pressure_bottom['time_0_reference_right']),lower_band_downstream_bottom, upper_band_downstream_bottom, alpha=0.3, color="#c5b0d5")
    
    axes[1].set_title("Downstream Pressure Readings")

    fig1.suptitle("Pressure Validation - Extremes")

    fig1.tight_layout()
    
    plt.show()

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 8))

    for i in range(len(axes)):

        for j in range(len(axes[0])):

            axes[i][j].set_xlabel("Time (s)")
            axes[i][j].set_ylabel("Pressure (mV)") 

            if i == 0:
                axes[i][j].set_ylim(-0.6, -0.40)

            else: 
                axes[i][j].set_ylim(-0.30, -0.15)

    sns.scatterplot(x=(symmetry_pressure_west['time_values_left'] - symmetry_pressure_west['time_0_reference_left']), y=(symmetry_pressure_west['values_left']), ax=axes[0][0], color="#1f77b4" ,label="-90°", s=10)
    
    axes[0][0].errorbar((symmetry_pressure_west['time_values_left'] - symmetry_pressure_west['time_0_reference_left']), symmetry_pressure_west['values_left'], yerr=abs(symmetry_pressure_west['values_left']*instrument_error), ls='none', capsize=2, capthick=0.15, color='black', alpha=0.5, linewidth = 0.15)

    model_symmmetry_upstream_west = np.full(len(symmetry_pressure_west['values_left']), np.mean(symmetry_pressure_west['values_left']))

    lower_band_downstream_west, upper_band_downstream_west = find_confidence_bands(symmetry_pressure_west['values_left'], model_symmmetry_upstream_west)

    sns.scatterplot(x=(symmetry_pressure_east['time_values_left'] - symmetry_pressure_east['time_0_reference_left']), y=(symmetry_pressure_east['values_left']), ax=axes[0][1], color="#2ca02c", label="90°", s=10)

    axes[0][1].errorbar((symmetry_pressure_east['time_values_left'] - symmetry_pressure_east['time_0_reference_left']), symmetry_pressure_east['values_left'], yerr=abs(symmetry_pressure_east['values_left']*instrument_error), ls='none', capsize=2, capthick=0.15, alpha=0.5, color='black', linewidth = 0.15)

    model_symmetry_downstream_east = np.full(len(symmetry_pressure_east['values_left']), np.mean(symmetry_pressure_east['values_left']))

    lower_band_downstream_east, upper_band_downstream_east = find_confidence_bands(symmetry_pressure_east['values_left'], model_symmetry_downstream_east)
    
    axes[0][0].fill_between(symmetry_pressure_west['time_values_left'] - symmetry_pressure_west['time_0_reference_left'] , lower_band_downstream_west, upper_band_downstream_west, alpha=0.3, color='#aec7e8') 

    axes[0][1].fill_between(symmetry_pressure_east['time_values_left'] - symmetry_pressure_east['time_0_reference_left'] , lower_band_downstream_east, upper_band_downstream_east, alpha=0.3, color="#98df8a") 

    axes[0][0].set_title("Upstream: -90°")
    axes[0][1].set_title("Upstream: 90°")






    sns.scatterplot(x=(symmetry_pressure_west['time_values_right'] - symmetry_pressure_west['time_0_reference_right']), y=(symmetry_pressure_west['values_right']), ax=axes[1][0], label="-90", color="#d62728", s=10)

    axes[1][0].errorbar((symmetry_pressure_west['time_values_right'] - symmetry_pressure_west['time_0_reference_right']), symmetry_pressure_west['values_right'], yerr=abs(symmetry_pressure_west['values_right']*instrument_error), ls='none', capsize=2, capthick=0.15, color='black', alpha=0.5, linewidth = 0.15)

    model_symmmetry_downstream_right = np.full(len(symmetry_pressure_west['values_right']), np.mean(symmetry_pressure_west['values_right']))

    lower_band_downstream_west, upper_band_downstream_west = find_confidence_bands(symmetry_pressure_west['values_right'], model_symmmetry_downstream_right)







    sns.scatterplot(x=(symmetry_pressure_east['time_values_right'] - symmetry_pressure_east['time_0_reference_right']), y=(symmetry_pressure_east['values_right']), ax=axes[1][1], label="90", color="#9467bd", s=10)

    axes[1][1].errorbar((symmetry_pressure_east['time_values_right'] - symmetry_pressure_east['time_0_reference_right']), symmetry_pressure_east['values_right'], yerr=abs(symmetry_pressure_east['values_right']*instrument_error), ls='none', capsize=2, capthick=0.15, alpha=0.5, color='black', linewidth = 0.15)

    model_symmetry_downstream_east = np.full(len(symmetry_pressure_east['values_right']), np.mean(symmetry_pressure_east['values_right']))

    lower_band_downstream_east, upper_band_downstream_east = find_confidence_bands(symmetry_pressure_east['values_right'], model_symmetry_downstream_east)




    axes[1][0].fill_between(symmetry_pressure_west['time_values_right'] - symmetry_pressure_west['time_0_reference_right'] , lower_band_downstream_west, upper_band_downstream_west, alpha=0.3, color='#ff9896') 

    axes[1][1].fill_between(symmetry_pressure_east['time_values_right'] - symmetry_pressure_east['time_0_reference_right'] , lower_band_downstream_east, upper_band_downstream_east, alpha=0.3, color="#c5b0d5") 


    axes[1][0].set_title("Downstream: -90°")
    axes[1][1].set_title("Downstream: 90°")

    fig.suptitle("Symmetry Analysis of Pressures")

    fig.tight_layout()

    plt.show()


if __name__ == "__main__":

    orientation_angles = [0, 30, 90, 120, 180, 210, 240, 270]  # check powerpoint slide for definition of 0 degrees

    run_folder_path = "analysis/data/opaque/5Jun"

    momentum_ratio_string = "momentum3"

    temp_string = "temp60"

    analyse_all_runs(run_folder_path, momentum_ratio_string, temp_string, orientation_angles)

    depth = "four_mm"

    # one_mm_sym_data = show_symmetry(run_folder_path, momentum_ratio_string, temp_string, orientation_angles, depth)

    # one_mm_ext_data = show_extremes(run_folder_path, momentum_ratio_string, temp_string, orientation_angles, depth)

    # analyse_pressures(run_folder_path, momentum_ratio_string, temp_string, orientation_angles)

    analyse_temperatures_sym_and_extremes(run_folder_path, momentum_ratio_string, temp_string, orientation_angles, depth)
