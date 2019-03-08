#!/usr/bin/env python
import os
import serial, time
import math
import struct
import sys
import datetime
import subprocess

__author__ = 'Tony Lin'

ser = serial.Serial('/dev/pts/16',  115200, timeout = 3)    #Open the serial port at 115200 baud
ser.flush()
ser.write('aps\n') #Turn off the AP
f = open ('output.csv', 'a')
f.write('Vin, Battery voltage, Battery current, Battery capacity, Efficiency\n')
while True:
    try:
        while True:
            ser.write('battery\n')
            battery_voltage = None
            battery_current = None
            battery_capacity = None
            EFF = None
            for line in ser.readlines():
                #print('line = %s' % line)
                if 'V:' in line:
                    battery_voltage=(line.split()[-2])
                    print('Battery voltage: %s' % battery_voltage)
                #else:
                #    print('No V in line')
                if 'I:' in line:
                    battery_current=(line.split()[-2])
                    print('Battery current: %s' % battery_current)
                if 'Charge:' in line:
                    battery_capacity=(line.split()[-2])
                    print('Battery capacity: %s' % battery_capacity)
            
            cmd = ['dut-control', 'ppvar_batt_mw', 'ppvar_sys_mw', 'ppvar_c0_vbus_mw', 'ppvar_c0_vbus_mv']
            out = subprocess.check_output(cmd)
            out_string = out.split('\n')
            if 'ppvar_batt_mw:' in out_string[0]:
                i = out_string[0].find(':')
                P_BAT = abs(float(out_string[0] [i + 1:]))
                print('P_BAT = %s' % P_BAT)
            else:
                print('can not find ppvar_batt_mw\n')
           
            if 'ppvar_c0_vbus_mv:' in out_string[1]:
                i = out_string[1].find(':')
                V_USBC = float(out_string[1] [i + 1:])
                print('V_USBC = %s' % V_USBC)
            else:
                print('can not find ppvar_c0_usbc_mv\n')
            
            if 'ppvar_c0_vbus_mw:' in out_string[2]:
                i = out_string[2].find(':')
                P_USBC = float(out_string[2] [i + 1:])
                print('P_USBC = %s' % P_USBC)
            else:
                print('can not find ppvar_c0_usbc_mw\n')
            
            if 'ppvar_sys_mw:' in out_string[3]:
                i = out_string[3].find(':')
                P_SYS = float(out_string[3] [i + 1:])
                print('P_SYS = %s\n' % P_SYS)
            else:
                print('can not find ppvar_sys_mw\n')

            EFF = (P_BAT + P_SYS) / P_USBC * 100
            print('The efficiency is: %.2f%%' % EFF)
            
            f.write('%.1f,%s,%s,%s,%.2f%%\n' % (V_USBC, battery_voltage, battery_current, battery_capacity, EFF))
            f.closed
            time.sleep(1)
    except IndexError:
        print("Unable to read")
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit(0)

