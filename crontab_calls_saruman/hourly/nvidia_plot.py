# encoding: utf-8

"""
Here we are going to create functions that can plot the results of nvidia text..
Can be used for a ... website?

Dit is dus echt kut. Ik haaaat pandas ...
Hopelijk kan t ook met numpy

Of plotted met pandas moet ik ff leren.
En moet natuurlijk ff bedenkn hoe ik dit dan kan embedded in een html pagina..
zou vet zijn als je pet plotly ofzo iets "interactiefs" kan doen.


What we learned here is that nuympy is a piece of shit when you deal with datetime objects.
Maybe I couldve used a different datetime thingybob but fuck that.
I wanted datetime
Now I need to use pnadas.
FIne.
"""

import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

path_to_csv = '/home/charmmaria/data/nvidia'
file_name = 'nvidia_database.csv'

divfun = lambda a: round(int(a[0])/int(a[1])*100)

# Read data
A = np.genfromtxt(os.path.join(path_to_csv, file_name), delimiter=',', dtype=str)
A_col = dict(zip(A[0], range(len(A[0]))))
A = A[1:]

# Create an empty dataframe...
B = pd.DataFrame(np.empty(A.shape))
B.columns = list(A_col.keys())

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
A_pwr_format = np.array([divfun(re.findall("([0-9]*)W/([0-9]*)W", x)[0]) for x in A_pwr])
B['Pwr:Usage/Cap'] = A_pwr_format

# Format Fan
A_fan = A[:, A_col['Fan']]
A_fan_format = np.array([int(x[:-1]) for x in A_fan])
B['Fan'] = A_fan_format

# Format Mem-Usage
A_mem = A[:, A_col['Memory-Usage']]
A_mem_format = np.array([divfun(re.findall("([0-9]*)MiB/([0-9]*)MiB", x)[0]) for x in A_mem])
B['Memory-Usage'] = A_mem_format

# Define plotting cols and unique GPU ids
plot_cols = ['Memory-Usage', 'Pwr:Usage/Cap', 'Temp', 'Fan']
A_ugpu = set(A_gpu)

# Display the things...
# Bar plots are insanely annoing. Need a test case of some sort to explore this..
for i, i_name in enumerate(plot_cols):
    for i_gpu in A_ugpu:
        index_gpu = B['GPU'] == i_gpu
        fig = plt.figure(i)
        #ax = fig.axes[0]
        plt.title(i_name)
        #ax.axvspan(B.loc[index_gpu, 'Time'].tolist()[0].date(), B.loc[index_gpu, 'Time'].tolist()[10].date(),
        # alpha=0.5)
        plt.plot(B.loc[index_gpu, 'Time'], B.loc[index_gpu, i_name], '.--')

    # B.loc[index_gpu, 'Time'][0]
    plt.xticks(rotation=45)

# B.loc[index_gpu, 'Time']
#
# for i in range(100):
#     plt.close()
