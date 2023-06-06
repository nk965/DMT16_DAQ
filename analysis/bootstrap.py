import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rd

data = pd.read_csv('c:/Users/jimty/Documents/University/Coursework/M03_DMT/DMT16_DAQ/analysis/data/opaque/5Jun/orientation4/temp60/momentum3/UNIT2-2023_06_05_17_43_36-CHANNEL2-temp.csv', header=0) # NOTE: Local location of .csv file

plt.rcParams["figure.figsize"] = [18,9.5] # Forming the Size of the Plot (and all future plots)

# Extract the data from the columns using the heading title names for the .csv read
temperature_data = data['temp_buffers'].to_numpy() # x represents the time index
time_data = data['times_ms_buffers'].to_numpy() # y represents the wavelength, measured in nanometres.
date_data = data['Time'].to_numpy()

plt.scatter(time_data, temperature_data, label='Raw')

# Assuming you have your original temperature values stored in a NumPy array called 'temperature_data'
mean = np.mean(temperature_data)
print('mean:', mean)
residuals = temperature_data - mean
variance = np.var(residuals)
print('var:', variance)

plt.axhline(mean)

# Set the number of bootstrap samples you want to generate
num_bootstraps = 1000

# Create an array to store the bootstrap temperature values
bootstrap_temperatures = np.empty_like(temperature_data)
bootstrapping_iter = 100
for n in range(bootstrapping_iter):
    resampled_data = [] # Initialising the resampled data
    for i in range(len(temperature_data)): # Iterating through the length of the input data i.e. all the data
        resample = np.random.choice(temperature_data, replace=True) + 0.1*np.random.normal(0,0.05**2)+0.008 # Producing and replacing a random new value given the input data
        resampled_data.append(resample) # Adding this new value to resampled_data to then be returned

# Generate bootstrap samples
# for i in range(num_bootstraps):
#     # Sample with replacement from the residuals
#     bootstrap_residuals = np.random.choice(residuals, size=len(residuals), replace=True)
    
#     # Add the bootstrap residuals to the mean to get bootstrap temperatures
#     bootstrap_temperatures = mean + bootstrap_residuals
    
#     # Save the bootstrap temperatures in the corresponding array positions
#     bootstrap_temperatures[i] = bootstrap_temperatures

plt.scatter(time_data, resampled_data, label='Bootstrap')

plt.axhline(np.mean(resampled_data), color='orange')

plt.legend()

plt.show()

print('mean', np.mean(resampled_data))
print('var', np.var(resampled_data))

data_new = [resampled_data,time_data,date_data]
for row in data_new:
    for item in row:
        print(item)