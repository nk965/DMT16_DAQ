import ctypes
import numpy as np
import time
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
from TC08_config import USBTC08_CONFIG, INPUT_TYPES

class LoggingUnit:
    
    def __init__(self, config, sampling_interval_input, recording_period) -> None:
        self.chandle = ctypes.c_int16()
        self.status = {}
        self.config = config
        self.results = {}
        self.sampling_interval_input = sampling_interval_input
        self.recording_period = recording_period

    def __repr__(self) -> str:
        return f'{self.config.keys()}: {self.status}'
            
    def openUnit(self):
        self.status["open_unit"] = tc08.usb_tc08_open_unit()
        assert_pico2000_ok(self.status["open_unit"])
        chandle = self.status["open_unit"]


if __name__ == "__main__":

    # set length recording in seconds

    sns.set_theme(style="darkgrid")

    recording_period = 20
    sampling_interval_ms = 300

    UNIT_1 = LoggingUnit(USBTC08_CONFIG["UNIT_1"], sampling_interval_ms, recording_period)

    UNIT_2 = LoggingUnit(USBTC08_CONFIG["UNIT_2"], sampling_interval_ms, recording_period)
    
    print(UNIT_1.__repr__)
    print(UNIT_2.__repr__)

    UNIT_1.openUnit()
    UNIT_2.openUnit()