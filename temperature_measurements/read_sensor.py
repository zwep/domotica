#! /usr/bin/env python3
import serial
import time
import datetime
import os
import requests
import json

# Needed to find the serial port
if os.path.exists('/dev/ttyACM0') == True:
        ser = serial.Serial(port='/dev/ttyACM0',baudrate = 115200,parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
        print("Serial device defined")
if os.path.exists('/dev/ttyACM1') == True:
        ser = serial.Serial(port='/dev/ttyACM1',baudrate = 115200,parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
        print("Serial device defined")

# Here we store the data in format (date, pin number, humidity, temp)
dest_file = '/home/pi/data_file.txt'

# Needed to compare inside to outside temp
def get_current_outside_temp():
        url_houten = 'http://weerlive.nl/api/json-data-10min.php?key=9031ec6a73&locatie=Houten'
        r = requests.get(url_houten, timeout=10, verify=False)
        content = r.content.decode("utf8")
        js = json.loads(content)
        return js['liveweer'][0]['temp']


# Reading the serial input and writing that data plus current outside temp
def write_append_fun():
        global ser
        print("Starting")
        while True:
                datetime_string = datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
                myData1 = ser.readline()
                myData1 = myData1.decode("utf-8", "ignore")
                humidity_temp = myData1.strip()
                if humidity_temp:
                        data_string = datetime_string + "\t" + humidity_temp + "\n"
                        with open(dest_file, 'a') as f:
                                f.write(data_string)


if __name__ == "__main__":
        # Do it
        write_append_fun()