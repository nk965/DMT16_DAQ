import os
import matplotlib.pyplot as plt

class Datalogger_Data:

    def readfile(self, file_path):
        # Change the text file

        with open(str(file_path), 'r') as read:
            x = read.read().splitlines()
        return x

    def __init__(self, file_path, depth, rotation_angles, location):  # change filename into filepath

        import numpy as np

        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.rotation_angle = rotation_angles
        self.depth = depth

        if location == 0:
            self.location = "Left"
        elif location == 1:
            self.location = "Right"
        else:
            self.location = str(location)

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
            time_microseconds = ((time[0] * 3600 + time[1] * 60 + time[2]) * 10 ** 6 + time[3]).astype(np.uint64)
            split_data[index][2] = time_microseconds

        self.data = split_data

    def print_status(self):
        print("File name : " + self.filename)
        print("%s, %s" % (self.unit, self.channel))
        print("Rotation Angle : " + str(self.rotation_angle))
        print("Depth : " + str(self.depth) + " mm")
        print("Location : " + self.location)
        print("%s, %s" % (self.date, self.start_time))
        print("Type: " + self.type)

    def print_data(self):
        print(self.data)


class GPIO_Data:

    def readfile(self, name):
        # Change the text file
        with open(name, 'r') as read:
            x = read.read().splitlines()
        return x

    def __init__(self, file_path):
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
        self.Pin8_data = []

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

            elif data[0] == "8":
                self.Pin8_data.append(data)

            elif data[0] == "16":
                self.Pin16_data.append(data)

            elif data[0] == "20":
                self.Pin20_data.append(data)

            elif data[0] == "21":
                self.Pin21_data.append(data)

        self.Pin1_data = np.asarray(self.Pin1_data)
        self.Pin8_data = np.asarray(self.Pin8_data)
        self.Pin16_data = np.asarray(self.Pin16_data)
        self.Pin20_data = np.asarray(self.Pin20_data)
        self.Pin21_data = np.asarray(self.Pin21_data)

    def print_status(self):
        print("File name : " + self.filename)
        print("%s, %s" % (self.date, self.start_time))
        print("Type: " + self.type)

    def print_data(self):
        print(self.Pin1_data)
        print(self.Pin12_data)
        print(self.Pin16_data)
        print(self.Pin20_data)
        print(self.Pin21_data)


# (unit,channel) -> (depth, initial angle before rotation, location)
# Depths are in mm
# Location 0 = left, 1 = right

null = -69

channel_info = {("UNIT1", "CHANNEL1"): (4, 0, 0),
                ("UNIT1", "CHANNEL2"): (3, 30, 0),
                ("UNIT1", "CHANNEL3"): (2, 60, 0),
                ("UNIT1", "CHANNEL4"): (1, 90, 0),
                ("UNIT1", "CHANNEL5"): (4, 0, 1),
                ("UNIT1", "CHANNEL6"): (3, 30, 1),
                ("UNIT1", "CHANNEL7"): (2, 60, 1),
                ("UNIT1", "CHANNEL8"): (1, 90, 1),
                ("UNIT1", "CHANNELCJC"): (null, null, null),

                ("UNIT2", "CHANNEL1"): (null, -30, 0),
                ("UNIT2", "CHANNEL2"): (null, -30, 1),
                ("UNIT2", "CHANNEL3"): (null, null, null),
                ("UNIT2", "CHANNEL4"): (null, null, null),
                ("UNIT2", "CHANNEL5"): (null, null, null),
                ("UNIT2", "CHANNEL6"): (null, null, null),
                ("UNIT2", "CHANNEL7"): (null, null, null),
                ("UNIT2", "CHANNEL8"): (null, null, null),
                ("UNIT2", "CHANNELCJC"): (null, null, null),
                }


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
    import numpy as np
    raw_data = data_class.data.astype(np.float64)
    temp_values = raw_data[:, 0]
    time_values_seconds = raw_data[:, 2] / (10 ** 6)
    return temp_values, time_values_seconds


def extract_GPIO_data(data_class):
    import numpy as np

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

    return [[Main_flow_meter_time_seconds, Main_flow_rate], [TB_motor_time_seconds, TB_motor_state],
                       [PIV_pulse_time_seconds, PIV_pulse_state], [Dye_injection_time_seconds, Dye_injection_state],
                       [Branch_flow_meter_time_seconds, Branch_flow_rate]]


if __name__ == "__main__":

    # Looking at data for a particular inlet condition 

    angle = [0, 30, 60]  
    folder_path = 'analysis/data/opaque/inlet1'
    test_runs = []

    # Obtain the CSV Files and create dataclasses for each test run with that inlet condition

    for index, test_run in enumerate(os.scandir(folder_path)):
        if test_run.name == '.DS_Store' or not test_run.is_dir():
            continue  # Skip .DS_Store file and non-directories

        subfolder_path = test_run.path
        print(f'Processing run at: {subfolder_path}')

        # append all classes in a list called test_runs 

        test_runs.append(process_individual_run(subfolder_path, angle[index]))

    # intialise individual arrays for sorting algorithm

    pressures = []
    
    four_mm = []
    
    three_mm = []
    
    two_mm = []
    
    one_mm = []
    
    temperatures = []
    
    GPIO_struct = []

    for run_number, run_info in enumerate(test_runs):
        for index, channels in enumerate(run_info):
            if channels.type == "temp":

                # If this is a pressure measurement:
                if channels.depth == null and (channels.rotation_angle - angle[
                    run_number]) != null and channels.location != null and channels.channel != "CHANNELCJC":
                    pressures.append(channels)

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
            
                GPIO_struct.append(channels)

    # Plotting GPIO data 

    labels = ["main flow rate", "TB motor", "PIV", "Dye Inject", "Branch Flow"]
    for struct in GPIO_struct:

        GPIO_run_data = extract_GPIO_data(struct)

        for index, run_data in enumerate(GPIO_run_data):

            plt.scatter(run_data[0], run_data[1],label=labels[index],s=1)
            plt.legend()

            plt.show()


    # plt.plot(extract_GPIO_data(GPIO_struct[0])[4][0], extract_GPIO_data(GPIO_struct[0])[4][1])
    # plt.show()

    # for test in pressures:
    #     test.print_status()

    # for test in four_mm:
    #     test.print_status()

    # for test in three_mm:
    #     test.print_status()

    # for test in two_mm:
    #     test.print_status()

    # for test in one_mm:
    #     test.print_status()

    # for test in temperatures:
    #     test.print_status()

    # print(pressures.print_status())
    # print(four_mm.print_status())
    # print(three_mm.print_status())
    # print(two_mm.print_status())
    # print(one_mm.print_status())
    # print(temperatures.print_status())