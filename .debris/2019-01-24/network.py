#!/usr/bin/env python
'''Everything related to Network Configuration & Testing'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

import visa
from time import time, ctime, sleep
from numpy import linspace

def checkall():
    '''Check the availability of all instrument
    '''
    rm = visa.ResourceManager()
    addresses = {}

    # listed (GPIB first):
    addresses["Yoko"] = "GPIB0::2::INSTR"

    # addresses["T01"] = "GPIB0::21::INSTR"
    # addresses["T02"] = "GPIB0::24::INSTR"
    # addresses["T03"] = "GPIB0::5::INSTR"

    addresses['RDS'] = 'TCPIP0::192.168.1.81::INSTR'
    addresses["PSG"] = 'TCPIP0::192.168.1.35::INSTR'
    addresses["ENA"] = 'TCPIP0::192.168.1.85::INSTR'
    # addresses["PNA"] = "TCPIP0::192.168.0.6::hpib7,16::INSTR"
    # addresses["MXG"] = "TCPIP0::192.168.0.3::INSTR"

    # addresses["VSA"] = "PXI22::12::0::INSTR;PXI22::14::0::INSTR;PXI22::8::0::INSTR;PXI22::9::0::INSTR;PXI27::0::0::INSTR"
    # addresses["AWG"] = "PXI20::14::0::INSTR"

    addresses['RDG'] = 'TCPIP0::192.168.1.179::INSTR'

    timelimit = 3000
    instr = {}
    for i,ad in addresses.items():
        try:
            start = time()
            instr[i] = rm.open_resource(ad)
            end = time()
            exectime = float(end - start)
            instr[i].read_termination = '\n' #omit termination tag from output 
            instr[i].timeout = min([exectime*30000, timelimit]) #set timeout
            print(Fore.WHITE + Back.GREEN + "%s is ONLINE!" %i)
            if i in ['Yoko']:
                print(Fore.YELLOW + "OD: %s" %instr[i].query('OD'))
            else:
                print(Fore.YELLOW + "ID: %s" %instr[i].query('*IDN?'))  #inquiring machine identity: "who r u?"
        except:
            pass
            print(Fore.RED + "%s is OFFLINE!" %i)

    return instr

instr = checkall()

GPIBspeed = 62 #pts/s
Sweeptime = 15 #s
points = int(GPIBspeed * Sweeptime)
instr['Yoko'].write('H0;F1;R6;OD') #No header; DC current in V; 30V range; Old value
instr['Yoko'].write('O1E') #OUTPUT ON
for V in linspace(0, -5, round(points/2)):
    print("V: %.5f" %V)
    instr['Yoko'].write('S%.5fE'%V) #Set Voltage
for V in linspace(-5, 0, round(points/2)):
    print("V: %.5f" %V)
    instr['Yoko'].write('S%.5fE'%V) #Set Voltage
sleep(3)
instr['Yoko'].write('O0E') #OUTPUT OFF

