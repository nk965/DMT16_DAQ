import os

# (unit,channel) -> (depth, initial angle before rotation, location)
# Depths are in mm
# Location 0 = left, 1 = right

null = -69
shift = -90

channel_info = {("UNIT1", "CHANNEL1"): (4, 90+shift, 0),
                ("UNIT1", "CHANNEL2"): (3, 60+shift, 0),
                ("UNIT1", "CHANNEL3"): (2, 30+shift, 0),
                ("UNIT1", "CHANNEL4"): (1, 0+shift, 0), # BEWARE OF SIGN CONVENTION - MADE IT MORE INTUITIVE NOT TIANHONG
                ("UNIT1", "CHANNEL5"): (4, 90+shift, 1),
                ("UNIT1", "CHANNEL6"): (3, 60+shift, 1),
                ("UNIT1", "CHANNEL7"): (2, 30+shift, 1),
                ("UNIT1", "CHANNEL8"): (1, 0+shift, 1),
                ("UNIT1", "CHANNELCJC"): (null, null, null),

                ("UNIT2", "CHANNEL1"): (null, -30+shift, 0), # pressure 
                ("UNIT2", "CHANNEL2"): (null, -30+shift, 1), # pressure
                ("UNIT2", "CHANNEL3"): (null, null, null), # Transparent 1
                ("UNIT2", "CHANNEL4"): (null, null, null), # Transparent 2 
                ("UNIT2", "CHANNEL5"): (null, null, null), # Transparent 3 
                ("UNIT2", "CHANNEL6"): (null, null, null), # Ambient Test
                ("UNIT2", "CHANNEL7"): (null, null, null), # Main Inlet
                ("UNIT2", "CHANNEL8"): (null, null, null), # Branch Inlet
                ("UNIT2", "CHANNELCJC"): (null, null, null),
                }
