# Importing Libraries
import sys
from datetime import datetime, date
import time
import numpy as np
import csv
import pigpio # Library for high speed gpio

# On Startup: $ sudo pigpiod
# Go to Directory
# To run: ~/Directory $ python3 GPIO.py 12 16
    # Numbers represent the pins being checked (leaving blank will check all pins)


last = [None]*32
cb = [] # Initialising list for data
py_data = [['GPIO','State','Tick','Diff']] # Titles

# Defining Callback Function, GPIO = Pin No., level = state (1=HIGH, 0=LOW), tick = time (in us) since RPi bootup
def cbf(GPIO, level, tick):
   if last[GPIO] is not None:
      diff = pigpio.tickDiff(last[GPIO], tick) # Time difference (in us) between the current event change and the last change
      py_data.append([GPIO, level, tick, diff])
      #print("G={} l={} t={} d={}".format(GPIO, level, tick, diff)) - Debug Printing - IGNORE
   last[GPIO] = tick # Resetting the new previous GPIO state and tick time

pi = pigpio.pi() # Connects to Local Pi

if not pi.connected: # Exits code if no connection
   exit()

if len(sys.argv) == 1:
   G = range(0, 32) # Total of 32 Pins
else:
   G = []
   for a in sys.argv[1:]:
      G.append(int(a)) # For running code on multiple systems - IGNORE
   
for g in G:
   cb.append(pi.callback(g, pigpio.EITHER_EDGE, cbf)) # Calls function once event change is detected on pin g

# Closing Procedure
try:
   while True:
      time.sleep(60)
except KeyboardInterrupt:
   print("\nTidying up")
   with open('time_GPIO' + str(date.today()) + '.csv', 'a+', newline='') as csvfile: # Writing Data into .csv
        writer = csv.writer(csvfile)
        for i in py_data:
            row = [i]
            writer.writerow(row) # Writing one row at a time
   for c in cb:
      c.cancel()

pi.stop()
