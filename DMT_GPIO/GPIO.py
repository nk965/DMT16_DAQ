# Importing Libraries
import sys
from datetime import datetime, date
import time
import numpy as np
import csv
import pigpio  # Library for high speed gpio

"""
@author: Jimmy van de Worp
This script receives high speed GPIO indefinitely and records the Pin Number, State, and Tick of each GPIO change detected

"""

'''

Current start-up procedure:
$ sudo pigpiod 
Go to Directory

Running procedure:

To run: ~/Directory $ python3 GPIO.py 12 16
Numbers represent the pins being checked (leaving blank will check all pins)
Defining Callback Function, GPIO = Pin No., level = state (1=HIGH, 0=LOW), tick = time (in us) since RPi bootup

'''

def procedure(GPIO, level, tick):

   '''
   This is the function that occurs when a GPIO change is detected in the pi.callback().
   It appends the GPIO Pin, State, Tick, and Time Difference since last State Change was detected to the py_data array.

    Returns:
        None 
   
   '''

   if last[GPIO] is not None:
   
      # Time difference (in us) between the current event change and the last change
   
      diff = pigpio.tickDiff(last[GPIO], tick)
   
      py_data.append([GPIO, level, tick, diff])
   
      # print("G={} l={} t={} d={}".format(GPIO, level, tick, diff)) - Debug Printing - IGNORE
   
   last[GPIO] = tick  # Resetting the new previous GPIO state and tick time


if __name__ == '__main__':

   last = [None]*32

   cb = []  # Documented Standard for library and pi.callback()
   
   py_data = [['GPIO', 'State', 'Tick', 'Diff']]  # Titles

   pi = pigpio.pi()  # Connects to Local Pi

   if not pi.connected:  # Exits code if no connection
     
      exit()

   if len(sys.argv) == 1:
   
      pins = range(0, 32)  # Total of 32 Pins
   
   else:
   
      pins = []
   
      for i in sys.argv[1:]:
   
         pins.append(int(i))  # For running code on multiple systems - IGNORE

   for pin in pins:
   
      # Calls function once event change is detected on pin g
   
      cb.append(pi.callback(pin, pigpio.EITHER_EDGE, procedure))

   # Closing Procedure

   try:

      while True:

         time.sleep(60) # Runs Indefinitely

   except KeyboardInterrupt: # Until Keyboard Interrupt

      print("\nTidying up")

      with open('time_GPIO' + str(date.today()) + '.csv', 'a+', newline='') as csvfile:  # Writing Data into .csv

         writer = csv.writer(csvfile)

         for i in py_data:

               row = [i]

               writer.writerow(row)  # Writing one row at a time

      for c in cb:

         c.cancel()

   pi.stop()
