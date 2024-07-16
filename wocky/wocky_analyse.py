import os
import matplotlib.pyplot as plt

import collections
import matplotlib.pyplot as plt
from datetime import datetime
import re
import itertools
from dateutil.parser import parse

#
# ddata = '/home/bugger/Documents/data/wocky/WhatsApp Chat - Wocky! 353 Knuffels!/_chat.txt'
#
# with open(ddata, 'r') as f:
#     A = f.readlines()
#
# index_celine = [i for i, x in enumerate(A) if 'céline' in x.lower()]

ddata = '/home/bugger/Documents/Thuis/trouwen/geloftes/whatsapp_seb/_chat.txt'
dstop = '/home/bugger/Documents/Thuis/trouwen/geloftes/dutch.txt'

with open(dstop, 'r') as f:
    dutch_stop = f.read()

dutch_stop = dutch_stop.split('\n')

with open(ddata, 'r') as f:
    seb_chat = f.readlines()


re_date_obj = re.compile('\[([0-9].*?)\]')

message_time = []
not_parsed = []
celine_counter = 0
celine_line_length = 0
seb_counter = 0
seb_line_length = 0
total_line_length = 0
for i_line in seb_chat:
    total_line_length += len(i_line)
    time_str = re_date_obj.findall(i_line)
    if time_str:
        if len(time_str[0]) > 4:
            datetime_obj = parse(time_str[0])  # datetime.strptime(time_str[0], '%d/%m/%Y, %H:%M:%S')
            message_time.append(datetime_obj)
    else:
        not_parsed.append(i_line)

    if ' Céline: ' in i_line:
        celine_counter += 1
        celine_line_length += len(i_line)
    if ' Seb Harrevelt: ' in i_line:
        seb_counter += 1
        seb_line_length += len(i_line)

print('seb message percentage', seb_counter / len(seb_chat))
print('ce message percentage', celine_counter / len(seb_chat))
print('seb text percentage', seb_line_length / total_line_length)
print('ce text percentage', celine_line_length / total_line_length)

all_words = list(itertools.chain(*[x.lower().split() for x in seb_chat]))
dutch_stop += ['céline:', ':', 'seb', 'harrevelt', 'harrevelt:', ':)']
all_words = [x for x in all_words if x not in dutch_stop]
counter_obj = collections.Counter(all_words)
counter_obj.most_common(60)

# Counts of messages
year_extr = [x.year for x in message_time]
dict(collections.Counter(year_extr))

year_month_extr = [str(x.year) + str(x.month) for x in message_time]
plt.plot(dict(collections.Counter(year_month_extr)).values())
