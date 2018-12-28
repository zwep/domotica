# encoding: utf-8

""" Netgear to mysql """


from config import *
import os
from netgear_code.get_netgear import get_netgear_devices
import sqlalchemy

seb_mysql_key = os.environ['seb_mysql_key']

# Obtaining netgear_code devices
A = get_netgear_devices()

# Create engine
engine = sqlalchemy.create_engine('mysql+pymysql://{user}:{password}@localhost/{db}'.format(user=MYSQL_USER,
                                                                                    password=seb_mysql_key,
                                                                                    db=DB_NAME_NETGEAR))

# Add data to the database
A.to_sql(DB_NAME_NETGEAR, con=engine, index=False, if_exists='append')


