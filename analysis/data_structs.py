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

        # Not sure - temporary fix
        self.Pin12_data = []

        split_data = np.asarray(split_data)

        for index, data in enumerate(split_data):
            time = np.asarray(data[4].split(":")).astype(np.uint64)
            time_microseconds = ((time[0] * 3600 + time[1] * 60 + time[2]) * 10 ** 6 + time[3]).astype(np.uint64)
            split_data[index][4] = time_microseconds

            if data[0] == "1":
                self.Pin1_data.append(data)

            elif data[0] == "8":
                self.Pin8_data.append(data)

            elif data[0] == "12":
                self.Pin12_data.append(data)

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


