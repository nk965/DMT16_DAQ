#!/bin/sh
# launcher.sh
# navigate to home directory, run pigpiod library, then to this directory, then execute python scripts, then back home

cd /
sudo pigpiod
cd home/icl-dmt16/DMT16_DAQ/DMT_RPi
python3 Serial.py
python3 Streaming.py & python3 GPIO.py 1 8 16 20 21
cd /
sudo killall pigpiod