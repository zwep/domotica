# encoding: utf-8

""" Testing netgear_code connection """

print('Starting script\n')
from pynetgear import Netgear
from elasticsearch import Elasticsearch
import os
from datetime import datetime
print('Loaded all libraries\n')
es = Elasticsearch()



for i in os.environ.keys():
    print(i)
netgear = Netgear(password=os.environ['netgear_key'])

for i in netgear.get_attached_devices():
    temp_dict = dict(zip(i._fields, list(i)))
    temp_dict['date'] = datetime.isoformat(datetime.now())
    es.index(index='netgear_code', body=temp_dict, doc_type='_doc')

# We remove this to reduce traffic...?
#traffic_dict = netgear_code.get_traffic_meter()
#traffic_dict['date'] = datetime.isoformat(datetime.now())
#es.index(index='netgear_code', body=traffic_dict, doc_type='_doc')

