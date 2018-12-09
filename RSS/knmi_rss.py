# encoding: utf-8

"""
Going to use some knwi weather stuff here..

https://github.com/EnergieID/KNMI-py
"""

import knmi
df = knmi.get_day_data_dataframe(stations=[260])
print(df.disclaimer)
print(df.stations)

