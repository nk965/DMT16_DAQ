import os

class Datalogger_Data:

    def readfile(self,file_path):
        # Change the text file

        with open(str(file_path), 'r') as read:
            x = read.read().splitlines()
        return x

    def __init__(self,file_path,rotation_angles): #change filename into filepath

        import numpy as np

        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.rotation_angle = rotation_angles

        filename_array = np.asarray(self.filename.split("-"))

        self.unit = filename_array[0]

        self.date = filename_array[1][:10]
        self.start_time = filename_array[1][11:]
        self.channel = filename_array[2]
        self.type = filename_array[3].split(".")[0]

        unprocessed_data = self.readfile(self.file_path)
        del unprocessed_data[0]

        split_data = []

        for data_list in unprocessed_data:
            split_data.append(data_list.split(","))

        split_data = np.asarray(split_data)

        for index, data in enumerate(split_data):
            time = np.asarray(data[2].split(":")).astype(np.uint64)
            time_microseconds = ((time[0]*3600 + time[1]*60 + time[2])*10**6 + time[3]).astype(np.uint64)
            split_data[index][2] = time_microseconds

        self.data = split_data

class GPIO_Data:

    def readfile(self,name):
        # Change the text file
        with open(name, 'r') as read:
            x = read.read().splitlines()
        return x

    def __init__(self,file_path):
        import numpy as np
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        filename_array = self.filename.split("-")
        self.date = filename_array[1][:10]
        self.start_time = filename_array[1][11:]
        filename_array[3] = filename_array[3].split(".")
        self.type = filename_array[3][0]

        unprocessed_data = self.readfile(self.file_path)
        del unprocessed_data[0]

        split_data = []

        for data_list in unprocessed_data:
            split_data.append(data_list.split(","))

        # Main flow meter
        self.Pin1_data = []

        # TB motor actuation
        self.Pin12_data = []

        # PIV Pulse
        self.Pin16_data = []

        # Dye injection actuation
        self.Pin20_data = []

        # Branch Flow Meter
        self.Pin21_data = []

        split_data = np.asarray(split_data)

        for index, data in enumerate(split_data):
            time = np.asarray(data[4].split(":")).astype(np.uint64)
            time_microseconds = ((time[0] * 3600 + time[1] * 60 + time[2]) * 10 ** 6 + time[3]).astype(np.uint64)
            split_data[index][4] = time_microseconds

            if data[0] == "1":
                self.Pin1_data.append(data)

            elif data[0] == "12":
                self.Pin12_data.append(data)

            elif data[0] == "16":
                self.Pin16_data.append(data)

            elif data[0] == "20":
                self.Pin20_data.append(data)

            elif data[0] == "21":
                self.Pin21_data.append(data)

        self.Pin1_data = np.asarray(self.Pin1_data)
        self.Pin12_data = np.asarray(self.Pin12_data)
        self.Pin16_data = np.asarray(self.Pin16_data)
        self.Pin20_data = np.asarray(self.Pin20_data)
        self.Pin21_data = np.asarray(self.Pin21_data)

def process_individual_run(folder_path):

    data_dump_experiment_path = folder_path

    experiment_data = []

    for filename in os.listdir(data_dump_experiment_path):
    
        if filename.endswith('.csv'):  # Filter CSV files

            file_path = os.path.join(data_dump_experiment_path, filename)

            filename_array = filename.split("-")

            if filename_array[0] == 'RPI':
                experiment_data.append(GPIO_Data(file_path))

            else: 
                experiment_data.append(Datalogger_Data(file_path, 30))
        
    return experiment_data

if __name__== "__main__":

    folder_path = 'analysis/data/opaque/inlet1'

    test_runs = []

    for test_run in os.scandir(folder_path):
        
        if test_run.is_dir():
            
            subfolder_path = test_run.path
            
            print(f'Processing run at: {subfolder_path}')

            test_runs.append(process_individual_run(subfolder_path))



# U2_CH2 = Datalogger_Data("UNIT2-2023_05_24_15_45_27-CHANNEL2-temp.csv",30)
# print(U2_CH2.data)
# print(U2_CH2.filename)
# print(U2_CH2.date)
# print(U2_CH2.unit)
# print(U2_CH2.type)
# print(U2_CH2.rotation_angle)
# print(U2_CH2.channel)
# print(U2_CH2.start_time)

# GPIO = GPIO_Data("RPI-2023_05_24_15_45_27-ALLPINS-GPIO.csv")
# print(GPIO.filename)
# print(GPIO.date)
# print(GPIO.type)
# print(GPIO.start_time)
# print(GPIO.Pin1_data)
# print(GPIO.Pin12_data)
# print(GPIO.Pin16_data)
# print(GPIO.Pin20_data)
# print(GPIO.Pin21_data)

# add material 