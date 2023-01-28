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
        self.chandle = ctypes.c_int16(tc08.usb_tc08_open_unit())
        self.config = config
        self.sampling_interval_input = sampling_interval_input
        self.recording_period = recording_period
        self.status = {}
        self.results = {}

    def __repr__(self) -> str:
        return f'{self.status}'

    def closeUnit(self) -> None:
        self.status["close_unit"] = tc08.usb_tc08_close_unit(self.chandle)
        assert_pico2000_ok(status["close_unit"])


if __name__ == "__main__":

    # set length recording in seconds

    sns.set_theme(style="darkgrid")

    recording_period = 20
    sampling_interval_ms = 300

    UNIT_1 = LoggingUnit(USBTC08_CONFIG["UNIT 1"], sampling_interval_ms, recording_period)

    UNIT_2 = LoggingUnit(USBTC08_CONFIG["UNIT 2"], sampling_interval_ms, recording_period)

    UNIT_1.closeUnit()
    UNIT_2.closeUnit()

    print(UNIT_1.__repr__)
    print(UNIT_2.__repr__)