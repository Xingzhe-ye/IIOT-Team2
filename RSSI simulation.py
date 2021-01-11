from random import choice
from random import shuffle
import pymssql
from collections import Iterable
import time

server = '140.118.199.95'
user = 'sa'
password = '789'
database = 'BLE'
port = '1433'
conn = pymssql.connect(server,user,password,database,port)
cursor = conn.cursor(as_dict=True)
while True:
    rssi_list = [-80,-80,-80]
    rssi = shuffle(rssi_list)
    T = time.ctime(time.time())
    ####Ra#########
    datatosql_A = [(T,rssi_list[0])]
    sql_A = 'INSERT INTO Ra(Time,RSSI) VALUES(%s,%d)'
    cursor.executemany(sql_A,datatosql_A)
    conn.commit()
    
    ####Rb#########
    datatosql_B = [(T,rssi_list[1])]
    sql_B = 'INSERT INTO Rb(Time,RSSI) VALUES(%s,%d)'
    cursor.executemany(sql_B,datatosql_B)
    conn.commit()
    
    ####Rc#########
    datatosql_C = [(T,rssi_list[2])]
    sql_C = 'INSERT INTO Rc(Time,RSSI) VALUES(%s,%d)'
    cursor.executemany(sql_C,datatosql_C)
    conn.commit()
    
    ####Rd#########
    # datatosql_D = [(T,rssi_list[3])]
    # sql_D = 'INSERT INTO Rd(Time,RSSI) VALUES(%s,%d)'
    # cursor.executemany(sql_D,datatosql_D)
    # conn.commit()
    
    time.sleep(4)