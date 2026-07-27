#!/usr/bin/env python3

import time
from libreVNA import libreVNA

# Create the control instance
vna = libreVNA('localhost', 19542)

# Quick connection check (should print "LibreVNA-GUI")
print(vna.query("*IDN?"))

# Make sure we are connecting to a device (just to be sure, with default settings the LibreVNA-GUI auto-connects)
dev = vna.query(":DEV:CONN?")
if dev == "Not connected":
    print("Not connected to any device, aborting")
    exit(-1)
else:
    print("Connected to "+dev)
    
# Create the calibrations measurements. This is necessary because the GUI starts with no calibration measurements by default.
# In case the GUI was already running, we clear the calibration measurements first.
vna.cmd("VNA:CAL:RESET")
vna.cmd("VNA:CAL:ADD OPEN")
vna.cmd("VNA:CAL:ADD SHORT")
vna.cmd("VNA:CAL:ADD LOAD")

# Set all three measurements to port 1 (just for clarity, 1 is already the default value)
vna.cmd("VNA:CAL:PORT 0 1")
vna.cmd("VNA:CAL:PORT 1 1")
vna.cmd("VNA:CAL:PORT 2 1")

def take_measurement(vna, cal_num):
    # start the measurement
    vna.cmd("VNA:CAL:MEAS "+str(cal_num))
    # wait for the measurement to complete
    while vna.query(":VNA:CAL:BUSY?") == "TRUE":
        time.sleep(0.1)

# Take the measurementss
input("Connect the OPEN standard and press ENTER to continue")
take_measurement(vna, 0);
input("Connect the SHORT standard and press ENTER to continue")
take_measurement(vna, 1);
input("Connect the LOAD standard and press ENTER to continue")
take_measurement(vna, 2);

# Activate the calibration
vna.cmd("VNA:CAL:ACT SOLT_1")

# Readback active calibration type
print("Active calibration: "+vna.query("VNA:CAL:ACTIVE?"))