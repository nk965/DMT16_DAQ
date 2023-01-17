import ctypes
import numpy as np
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
from TC08_config import USBTC08_CHANNELS

USBTC08_MAX_CHANNELS = 8 #Max number of channels

# Use streaming mode
def streaming_mode():
    # Create chandle and status ready for use
    chandle = ctypes.c_int16()
    status = {}

    # open unit
    status["open_unit"] = tc08.usb_tc08_open_unit()
    assert_pico2000_ok(status["open_unit"])
    chandle = status["open_unit"]

    # set mains rejection to 50 Hz
    status["set_mains"] = tc08.usb_tc08_set_mains(chandle,0)
    assert_pico2000_ok(status["set_mains"])

    #Use Type K Thermocouples and set channels

    typeK = ctypes.c_int8(75)

if __name__ == "__main__":
    streaming_mode()

    # close unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])