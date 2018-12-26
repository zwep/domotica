from flask import Flask, render_template

from pynetgear import Netgear
import config
import re
import os

app = Flask(__name__)
netgear = Netgear(password=os.environ['netgear_key'])
name_list = ['seb', 'ella', 'ayla', 'barbara', 'noortje', 'joyce']


def get_netgear():
    res_dict = []
    for i in netgear.get_attached_devices():
        temp_dict = dict(zip(i._fields, list(i)))
        res_dict.append(temp_dict)
    return res_dict

def parse_activity(name_list, netgear_dict):

    active_name_list = [i_con['name'] for i_con in netgear_dict]
    res = []
    for roomy in name_list:
        temp = [True if re.match(roomy, y) else False for y in active_name_list]
        if any(temp):
            res.append(1)
        else:
            res.append(0.2)
    return res


@app.route('/')
def home():
    """
    Render the home page
    :return:
    """
    netgear_dict = get_netgear()
    print(netgear_dict)
    opacity_list = parse_activity(name_list, netgear_dict)

    return render_template('image_column.html', name_list=name_list, opacity_list=opacity_list)
