#!/usr/bin/env python
import minimalmodbus
import time
import serial
import requests
from datetime import datetime
import socketio
host_address = 'http://192.168.1.24:3000'


# port name, slave address (in decimal)
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1, 'rtu', True)

instrument.serial.baudrate = 9600 # Baud
sio = socketio.Client()
sio.connect("http://192.168.1.24:3000")
instrument.serial.timeout = 1 # seconds
print(instrument)

def send_data():    
    # Register number, number of decimals, function code
    parameters = instrument.read_registers(0, 10, 4)
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M:%S")

    ph = parameters[0]/100
    orp = parameters[4]
    temp = parameters[8]/10
    #print(date, time, ph, ordd, temp)
    
    data_send = {}
    for k in ('ph', 'orp', 'temp', 'date', 'time'):
        data_send[k] = locals()[k]

    try:
        sio.emit("DEVICE_SENDER",data_send)
        #print(res.text)
    except:
        print("connection failed")
        
#sleep for desired amount of time
if __name__ == "__main__":
    while True: 
        send_data()
        time.sleep(1)