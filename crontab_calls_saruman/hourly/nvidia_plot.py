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


def smooth(x, window_len=11, window='hanning'):
    """
    https://scipy-cookbook.readthedocs.io/items/SignalSmooth.html

    smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('numpy.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y


if os.name == 'nt':
    windows_system = True
else:
    windows_system = False

if windows_system:
    path_to_csv = r'C:\Users\20184098\Documents\data\nvidia'
else:
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
A_ugpu = list(set(A_gpu))

# Display the things...
# Bar plots are insanely annoing. Need a test case of some sort to explore this..
for i, i_name in enumerate(plot_cols):

    img_list = []
    for i_gpu in A_ugpu:
        index_gpu = B['GPU'] == i_gpu
        t_time = B.loc[index_gpu, 'Time']
        y = B.loc[index_gpu, i_name].rolling(28).mean()
        img_list.append(y)

    fig = plt.figure(i)
    fig.suptitle(i_name, fontsize=16)
    plt.subplot(131)
    plt.plot(t_time, img_list[0], 'r', label='GPU number' + A_ugpu[0])
    plt.legend()
    plt.xticks(rotation=45)
    plt.subplot(132)
    plt.plot(t_time, img_list[1], 'g', label='GPU number' + A_ugpu[1])
    plt.legend()
    plt.xticks(rotation=45)
    plt.subplot(133)
    plt.plot(t_time, img_list[2], 'b', label='GPU number' + A_ugpu[2])
    plt.legend()
    plt.xticks(rotation=45)



windows = ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']
for w in windows:
    t_time = B.loc[index_gpu, 'Time']
    y = B.loc[index_gpu, i_name].rolling(28).mean()
    y_smooth = smooth(y, 10, w)
    len(y_smooth[:-9])
    len(y)
    plt.plot(y - y_smooth[:-9])
    plt.plot(t_time, y, '-', label=w)
    plt.legend()
    plt.pause(5)
plt.show()
# B.loc[index_gpu, 'Time']
#
# for i in range(100):
#     plt.close()
