# encoding: utf-8

""" Testing netgear_code connection """


from config import *
import MySQLdb
import os
import db_management.mysql.check_content as check_mysql
from netgear_code.get_netgear import get_netgear_devices
import sqlalchemy

seb_mysql_key = os.environ['seb_mysql_key']

# Obtaining netgear_code devices
A = get_netgear_devices()

# Create engine
engine = sqlalchemy.create_engine('mysql://{user}:{password}@localhost/{db}'.format(user=MYSQL_USER,
                                                                                    password=seb_mysql_key,
                                                                                    db=DB_NAME_NETGEAR))

# Add data to the database
A.to_sql('netgear', con=engine, index=False, if_exists='append')


