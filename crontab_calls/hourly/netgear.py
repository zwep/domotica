# encoding: utf-8

""" Testing netgear connection """

print('Starting script\n')
from pynetgear import Netgear
from elasticsearch import Elasticsearch
import os
from datetime import datetime
print('Loaded all libraries\n')
es = Elasticsearch()
print('Setup elasticsearch \n')

print('Environmental keys')
for i in os.environ.keys():
    print(i)
netgear = Netgear(password=os.environ['netgear_key'])
print('Logged in with username: ', netgear.username)

print('Searching for devices')
for i in netgear.get_attached_devices():
    temp_dict = dict(zip(i._fields, list(i)))
    temp_dict['date'] = datetime.isoformat(datetime.now())
    es.index(index='netgear', body=temp_dict, doc_type='_doc')

print('Devices have been found')

traffic_dict = netgear.get_traffic_meter()
traffic_dict['date'] = datetime.isoformat(datetime.now())
es.index(index='netgear', body=traffic_dict, doc_type='_doc')

print('traffic meter as well')

