#!/usr/bin/env python

import pprint
from toon import Toon
import requests
import domotica_config as cnf

username, password = cnf.API_KEY_DICT['toon']

toon = Toon(username, password)
toon.set_maxretries(5)
toon.login()

thermostat = toon.get_thermostat_info()
temp = float(thermostat["currentTemp"]) / 100
print("current_temp:%.2f" % temp)

power = toon.get_power_usage()
print("current_powerusage:%d" % power["value"])

toon.logout()
