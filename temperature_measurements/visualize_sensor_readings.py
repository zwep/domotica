import os
import numpy as np
import datetime
import matplotlib.pyplot as plt

ddata = '/home/bugger/Documents/data/temperature_sensor/data_file.txt'

with open(ddata, 'r') as f:
    data_lines = f.readlines()


def parse_line(x):
    current_year = str(datetime.datetime.now().year)

    date_str_split = x.strip().split('\t')
    date_str = date_str_split[0]
    content_str = date_str_split[1:]
    if len(date_str) == 14:
        datetime_obj = datetime.datetime.strptime(current_year + "-" + date_str, '%Y-%m-%d|%H:%M:%S')
    else:
        datetime_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d|%H:%M:%S')
    if content_str[0].isdigit():
        humidity = float(content_str[1])
        temperature = float(content_str[2])
    else:
        datetime_obj = humidity = temperature = None

    return datetime_obj, humidity, temperature


date_array, humid_array, temp_array = zip(*[parse_line(i_line) for i_line in data_lines])
date_array = np.array([x for x in date_array if x])
humid_array = np.array([x for x in humid_array if x])
temp_array = np.array([x for x in temp_array if x])

import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%H:%M')


# # # Plot the stuff...
# GEt the sunrise
# Get the outside temp

from astral import LocationInfo
import datetime
from astral.sun import sun
city_obj = LocationInfo("Amsterdam")
sun_obj = sun(city_obj.observer, date=datetime.datetime.now())

sunrise_time = sun_obj['sunrise']


fig, ax = plt.subplots()
ax_deux = ax.twinx()
ax.xaxis.set_major_formatter(myFmt)

ax_temp = ax.plot(date_array, temp_array, 'r', label='temperature')
ax_humid = ax_deux.plot(date_array, humid_array, label='humidity')

ax.set_ylabel('Temperatuur (°C)')
ax_deux.set_ylabel('%humidity')

ax.text(sunrise_time, max(temp_array), 'sunrise')
ax.vlines(sunrise_time, ymin=min(temp_array), ymax=max(temp_array), colors='k', linestyles='--')

fig.suptitle('Temperature and humidity plot')

lns = ax_temp + ax_humid
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)
