# encoding: utf-8

""" Netgear to mysql """


import os
import sys
import sqlalchemy

if '__file__' in vars():
    project_path = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, os.path.pardir))
    print('Adding path: ', project_path)
    sys.path.append(project_path)

from netgear_code.get_netgear import get_netgear_devices
from config import *

seb_mysql_key = os.environ['seb_mysql_key']

# Obtaining netgear_code devices
A = get_netgear_devices()

# Create engine
engine = sqlalchemy.create_engine('mysql+pymysql://{user}:{password}@localhost/{db}'.format(user=MYSQL_USER,
                                                                                    password=seb_mysql_key,
                                                                                    db=DB_NAME_NETGEAR))

# Add data to the database
A.to_sql(TABLE_NAME_NETGEAR, con=engine, index=False, if_exists='append')


