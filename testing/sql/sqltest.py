import sys
import os
import time
import pymysql.cursors


## Credential
HOST = 'localhost' # MySQL server host DNS
PORT = 3306 # MySQL server port number
USER = 'greenhope' # MySQL account name
PASSWORD = 'Nahwals1234' # Password of the account
DB = 'greenhope' # DB name
TABLE = 'prototype' # table name
## Credential

connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, port=PORT) # make a connection to MySQL server

cursor = connection.cursor() # Open cursur to execute SQL query

def querygen(timestamp, sensor, measurement, value):
    return f"INSERT INTO {TABLE} (timestamp,sensor,measurement,value) VALUE('{timestamp}','{sensor}','{measurement}','{value}');"

query = querygen(time.strftime('%Y-%m-%d %H:%M:%S'), "debug", "test", 10)
print(query)
cursor.execute(query)
connection.commit()
print("done!")

