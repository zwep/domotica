# encoding: utf-8

""" Testing netgear connection """

from pynetgear import Netgear
from elasticsearch import Elasticsearch
import os
from datetime import datetime
es = Elasticsearch()

netgear = Netgear(password=os.environ['netgear_key'])
print('We are logged in with username: ', netgear.username)

for i in netgear.get_attached_devices():
    temp_dict = dict(zip(i._fields, list(i)))
    temp_dict['date'] = datetime.isoformat(datetime.now())
    es.index(index='netgear', body=temp_dict, doc_type='_doc')

print('attached devices have been connected')

traffic_dict = netgear.get_traffic_meter()
traffic_dict['date'] = datetime.isoformat(datetime.now())
es.index(index='netgear', body=traffic_dict, doc_type='_doc')

print('traffic meter as well')

