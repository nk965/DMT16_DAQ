import os

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
