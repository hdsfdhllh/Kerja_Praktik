#inisialisasi library yang digunakan
import urllib.request
import requests
import threading
import json
import random
import serial
import time
import datetime
import os
import glob

#inisialisasi dan setting code untuk pembacaan data sensor suhu
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        print(temp_c)
        return temp_c

#setting code untuk pengambilan data sensor PH dari serial monitor arduino uno
def a():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            a,b = line.split(',')
            print(a)
            return a

#setting code untuk pengambilan data sensor kekeruhan dari serial monitor arduino uno
def b():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            a,b = line.split(',')
            print(b)
            return b
            
#setting code untuk pengiriman data 3 sensor ke thingsepak
def thingspeak_post():
    threading.Timer(15,thingspeak_post).start()
    URL= 'https://api.thingspeak.com/update?api_key='
    KEY= '3PU8JQMR0NLV4V4Z'
    HEADER='&field1={}&field2={}&field3={}'.format(read_temp(),a(),b())
    NEW_URL= URL+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)
    print(data)
    
#setting code untuk memulai sistem
if __name__ == '__main__':
    thingspeak_post()
