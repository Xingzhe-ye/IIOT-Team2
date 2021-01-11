import numpy as np
import pymssql
from collections import Iterable
import time
from threading import Thread as thread
import time

#SQL collection
server = '140.118.199.95'
user = 'sa'
password = '789'
database = 'BLE'
port = '1433'
conn = pymssql.connect(server,user,password,database,port)
cursor = conn.cursor(as_dict=True)
state_list = ['Lab', 'Meeting Room', 'Classroom', 'Workshop', 'Fixed']


#current_state = state_list[4]
current_list = [state_list[4] for i in range(4)]


while(True):
    t1 = time.time()
    sql = 'select Time,RSSI from Ra where Time = (select max(Time) as maxtime from Ra)'
    cursor.execute(sql)
    RSSI_A_list = cursor.fetchall()
        
    sql = 'select Time,RSSI from Rb where Time = (select max(Time) as maxtime from Rb)'
    cursor.execute(sql)
    RSSI_B_list = cursor.fetchall()
    
    sql = 'select Time,RSSI from Rc where Time = (select max(Time) as maxtime from Rc)'
    cursor.execute(sql)
    RSSI_C_list = cursor.fetchall()
    
    sql = 'select Time,RSSI from Rd where Time = (select max(Time) as maxtime from Rd)'
    cursor.execute(sql)
    RSSI_D_list = cursor.fetchall()
    for a in RSSI_A_list:
        RSSI_A = a['RSSI']    
    conn.commit()
    if RSSI_A <= -70:
        A = state_list[4]
    else:
        A = state_list[0]
    
    for b in RSSI_B_list:
        RSSI_B = b['RSSI']
    conn.commit()
    if RSSI_B <= -70:
        B = state_list[4]
    else:
        B = state_list[1]
        
    for c in RSSI_C_list:
        RSSI_C = c['RSSI']    
    conn.commit()
    if RSSI_C <= -70:
        C = state_list[4]
    else:
        C = state_list[2]
        
    for d in RSSI_D_list:
        RSSI_D = d['RSSI']    
    conn.commit()
    if RSSI_D <= -70:
        D = state_list[4]
    else:
        D = state_list[3]
        
    state = [A,B,C,D]
    time.sleep(0.97)
    # print(state)
    
    for x in state:
        if x != "Fixed":
            print(x)
            Time = time.ctime(time.time())
            datatosql = [(Time, x)]
            sql = 'Insert INTO State_A(Time, State) VALUES(%s, %s)'
            cursor.executemany(sql, datatosql)
            conn.commit()

