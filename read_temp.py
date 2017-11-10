#!/usr/bin/env python
import os
import serial, time
import math
import struct
import sys
import datetime

__author__ = 'Tony Lin'

#Open the serial port at 115200 baud
ser = serial.Serial('/dev/pts/40',  115200, timeout = 1)    #Open the serial port at 115200 baud
#init serial
ser.flush()
f = open ('output.csv', 'a')
f.write('Battery temp, Charger temp, Battery voltage, Battery current, Battery capacity\n')
while True: 
    try:
        ser.write('temp\n')
        while True:
            line = ser.readline()
            if 'Battery' in line:
                battery_temp=(line.split()[-2])
                print('Battery temp:', battery_temp)
            if 'Charger' in line:
                charger_temp=(line.split()[-2])
                print('Charger temp:', charger_temp)
                break
        ser.write('battery\n')
        while True:
            line = ser.readline()
            if 'V:' in line:
                battery_voltage=(line.split()[-2])
                print('Battery voltage', battery_voltage)
            if 'I:' in line:
                battery_current=(line.split()[-2])
                print('Battery current:', battery_current)
            if 'Charge:' in line:
                battery_capacity=(line.split()[-2])
                print('Battery capacity', battery_capacity)
                break
        f.write('%s,%s,%s,%s,%s\n' % (battery_temp, charger_temp, battery_voltage, battery_current, battery_capacity))
        f.closed
        time.sleep(1)

    except IndexError:
        print("Unable to read")
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit(0)
