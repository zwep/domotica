# encoding: utf-8

"""
Here we create the plots from the nvidia_database.csv

We can filter on time.

Plots are saved automatically
"""

import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from matplotlib.pyplot import cm

# Choosing the right system
file_name = 'nvidia_database.csv'
if os.name == 'nt':
    windows_system = True
else:
    windows_system = False

if windows_system:
    path_to_csv = r'C:\Users\20184098\Documents\data\nvidia'
    path_to_plot = r'C:\Users\20184098\Pictures\pycharm\saruman'
else:
    #path_to_csv = '/home/charmmaria/data/nvidia'
    # path_to_csv = '/home/bugger/Documents/data/nvidia_saruman'
    path_to_csv = '/home/bugger/Documents/data/nvidia_boromir'
    path_to_plot = path_to_csv

# Simple function definition
divfun = lambda a: round(int(a[0])/int(a[1])*100)

# Read data
A = np.genfromtxt(os.path.join(path_to_csv, file_name), delimiter=',', dtype=str)
A_col = dict(zip(A[0], range(len(A[0]))))
A = A[1:]

# Create an empty dataframe...
B = pd.DataFrame(np.empty(A.shape))
B.columns = list(A_col.keys())

# ====================
# Format procedure
# ====================

# Format GPU column
A_gpu = A[:, A_col['GPU']]
B['GPU'] = A[:, A_col['GPU']].astype(str)

# Format time..
A_time = A[:, A_col['Time']]
A_time_format = np.array([datetime.datetime.strptime(x, "%Y_%m_%d %H:%M") for x in A_time])
B['Time'] = A_time_format

# Format temp...
A_temp = A[:, A_col['Temp']]
A_temp_format = np.array([int(x[:-1]) for x in A_temp])
B['Temp'] = A_temp_format

# Format Pwr
A_pwr = A[:, A_col['Pwr:Usage/Cap']]
A_pwr_format = np.array([divfun(re.findall("(-[0-9]*|[0-9]*)W/(-[0-9]*|[0-9]*)W", x)[0]) for x in A_pwr])
np.argmin(A_pwr_format)
B['Pwr:Usage/Cap'] = A_pwr_format

# Format Fan
A_fan = A[:, A_col['Fan']]
A_fan_format = np.array([int(x[:-1]) if x[:-1].isdigit() else -10 for x in A_fan])  ## Checken
# (A_fan_format == 150).sum()
B['Fan'] = A_fan_format
# (B['Fan'] == 150).sum()

# Format Mem-Usage
A_mem = A[:, A_col['Memory-Usage']]
A_mem_format = np.array([divfun(re.findall("(-[0-9]*|[0-9]*)MiB/(-[0-9]*|[0-9]*)MiB", x)[0]) for x in A_mem])
B['Memory-Usage'] = A_mem_format

# Define plotting cols and unique GPU ids
plot_cols = ['Memory-Usage', 'Pwr:Usage/Cap', 'Temp', 'Fan']
plot_names = ['memory_usage', 'power_usage', 'temp', 'fan']
A_ugpu = sorted(list(set(A_gpu)))


# ====================
# Plotting procedure
# ====================

# Display the things...
# Bar plots are insanely annoing. Need a test case of some sort to explore this..
filter_time = True
plt.close('all')
if filter_time:
    print('We are filtering on time!!')

for i, i_name in enumerate(plot_cols):

    # Collect data in one list
    img_list = []
    for i_gpu in A_ugpu:
        index_gpu = B['GPU'] == i_gpu
        t_time = B.loc[index_gpu, 'Time']
        # y = B.loc[index_gpu, i_name].rolling(28).mean()
        y = B.loc[index_gpu, i_name]
        img_list.append(y)

    # Filter on time.. since we dont want ALL the history.
    if filter_time:
        n_week = 12
        neg_week = datetime.timedelta(weeks=n_week)
        zero_time = datetime.datetime.today() - neg_week
        t_time_ind = t_time >= zero_time
        t_time = t_time[t_time_ind]
        img_list = [x.loc[t_time_ind.values] for x in img_list]

    # Plot the (filtered) data
    fig, ax_list = plt.subplots(ncols=len(img_list), num=i, figsize=(15, 10))
    fig.suptitle(i_name, fontsize=16)
    #   Plot style properties
    min_value = int(np.min(img_list)) - 5
    max_value = int(np.max(img_list)) + 5
    print(i_name, max_value)
    # color_list = ['r', 'g', 'b']
    color_list = cm.rainbow(np.linspace(0, 1, len(img_list)))

    for i_plot, i_img in enumerate(img_list):
        plot_name = 'GPU number' + A_ugpu[i_plot]
        y_plot = img_list[i_plot]
        ax_temp = ax_list[i_plot]
        xaxis_temp = ax_temp.get_xaxis()

        ax_temp.plot(t_time, y_plot, c=color_list[i_plot], label=plot_name)
        ax_temp.set_xticklabels(labels=t_time, rotation=45)
        ax_temp.set_ylim([min_value, max_value])
        ax_temp.title.set_text(plot_name)

        xaxis_temp.set_major_formatter(mdates.DateFormatter("%m-%d"))
        xaxis_temp.set_major_locator(mdates.DayLocator(interval=7))

    fig.legend()
    plt.savefig(os.path.join(path_to_plot, plot_names[i] + '.png'))
