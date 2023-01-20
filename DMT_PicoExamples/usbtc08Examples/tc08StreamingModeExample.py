#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# TC-08 STREAMING MODE EXAMPLE


import ctypes
import numpy as np
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok

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

# set up channel
# thermocouples types and int8 equivalent
# B=66 , E=69 , J=74 , K=75 , N=78 , R=82 , S=83 , T=84 , ' '=32 , X=88 
typeK = ctypes.c_int8(75)
status["set_channel"] = tc08.usb_tc08_set_channel(chandle, 1, typeK)
assert_pico2000_ok(status["set_channel"])

status["set_channel"] = tc08.usb_tc08_set_channel(chandle, 0, ctypes.c_int8(32))

assert_pico2000_ok(status["set_channel"])

# get minimum sampling interval in ms
status["get_minimum_interval_ms"] = tc08.usb_tc08_get_minimum_interval_ms(chandle)
assert_pico2000_ok(status["get_minimum_interval_ms"])

# set tc-08 running
status["run"] = tc08.usb_tc08_run(chandle, status["get_minimum_interval_ms"])
assert_pico2000_ok(status["run"])

time.sleep(2)

# collect data 
temp_buffer = (ctypes.c_float * 2 * 15)()

times_ms_buffer = (ctypes.c_int32 * 15)()

overflow = ctypes.c_int16()

status["get_temp"] = tc08.usb_tc08_get_temp_deskew(chandle, ctypes.byref(temp_buffer), ctypes.byref(times_ms_buffer), 15, ctypes.byref(overflow), 1, 0, 1)

#status["get_temp"] is the number of temperature samples in the buffer

assert_pico2000_ok(status["get_temp"])

np_temp_buffer = np.asarray(temp_buffer)
print(np_temp_buffer)

np_times_ms_buffer = np.asarray(times_ms_buffer)
print(np_times_ms_buffer)

temp_buffer_CJC = (ctypes.c_float * 2 * 15)()

times_ms_buffer_CJC = (ctypes.c_int32 * 15)()

overflow_CJC = ctypes.c_int16()

status["get_temp_2"] = tc08.usb_tc08_get_temp_deskew(chandle, ctypes.byref(temp_buffer), ctypes.byref(times_ms_buffer), 15, ctypes.byref(overflow), 0, 0, 1)

print(tc08.usb_tc08_get_last_error(chandle))

assert_pico2000_ok(status["get_temp_2"])

np_temp_buffer_CJC = np.asarray(temp_buffer_CJC)
print(np_temp_buffer_CJC)

np_times_ms_buffer_CJC = np.asarray(times_ms_buffer_CJC)
print(np_times_ms_buffer_CJC)

#if time.sleep(1), 5 readings
#if time.sleep(3), 15 readings
#if time.sleep(5), 15 readings, I think overflow is happening

# stop unit
status["stop"] = tc08.usb_tc08_stop(chandle)
assert_pico2000_ok(status["stop"])

# close unit
status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
assert_pico2000_ok(status["close_unit"])

# display status returns
print(status)