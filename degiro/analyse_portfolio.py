import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

ddata = '/media/bugger/MyBook/data/degiro'

waarde_list = []
for i_file in sorted(os.listdir(ddata)):
    file_dir = os.path.join(ddata, i_file)
    csv_obj = pd.read_csv(file_dir, decimal=",")
    tot_waarde = csv_obj['Waarde in EUR'].sum()
    waarde_list.append(tot_waarde)

plt.plot(waarde_list)