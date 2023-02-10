# Importing Libraries
import sys
import time
import numpy as np
import pigpio # Library for high speed gpio

last = [None]*32
cb = [] # Initialising list for data
py_data = [['GPIO','State','Tick','Diff']]

# Defining Storage Function to append each generated list
#def storage(datalist):
#   print(datalist)

# Defining Callback Function, GPIO = Pin No., level = state (1=HIGH, 0=LOW), tick = time (in us) since RPi bootup
def cbf(GPIO, level, tick):
   if last[GPIO] is not None:
      diff = pigpio.tickDiff(last[GPIO], tick) # Time difference (in us) between the current event change and the last change
      datalist = [GPIO, level, tick, diff]
      #print("G={} l={} t={} d={}".format(GPIO, level, tick, diff))
   last[GPIO] = tick # Resetting the new previous GPIO state and tick time

pi = pigpio.pi() # Connects to Local Pi

if not pi.connected: # Exits code if no connection
   exit()

if len(sys.argv) == 1:
   G = range(0, 32) # Total of 32 Pins
else:
   G = []
   for a in sys.argv[1:]:
      G.append(int(a)) # For multiple systems - ignore
   
for g in G:
   cb.append(pi.callback(g, pigpio.EITHER_EDGE, cbf)) # Calls function once event change is detected on pin g
   print(len(cb))
   py_data.append(cb)

# Closing Procedure
try:
   while True:
      time.sleep(60)
except KeyboardInterrupt:
   print("\nTidying up")
   np_data = np.array(py_data)
   print(np_data)
   for c in cb:
      c.cancel()

pi.stop()
