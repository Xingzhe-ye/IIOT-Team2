from scipy.ndimage import gaussian_filter1d as gsfilter
from bluepy.btle import Scanner
import time
import numpy as np 
import math
import pymssql
from collections import Iterable

server = "140.118.199.95"
user = "sa"
password = "789"
database = "BLE"
port = "1433"
conn = pymssql.connect(server,user,password,database,port)
cursor = conn.cursor(as_dict=True)

while True:
    scanner = Scanner()
    t = 0.5  #time of scanning
    add = "ac:23:3f:5a:a5:3c"    #item of scanning device
    
    RSSI = []
    t1 = time.time()
    print("RSSI Decting...(unit:dbm)")
    while True:
        devices = scanner.scan(t)
        for device in devices:
            if device.addr == add:
                RSSI += [device.rssi]
                print(device.rssi)
        if time.time()-t1 >=4:break
    print(RSSI) 

    if len(RSSI)>=3:
        rssi = RSSI
    else:
        rssi = [-201,-200,-200,-199]

    print(rssi) 
    rssi.remove(np.min(rssi))
    rssi.remove(np.max(rssi))
    print(rssi)
    r = np.array(rssi)
    R = round(np.mean(r),3)
    print(R)
    Time = time.ctime(time.time())

    datatosql = [(Time,R)]
    sql = "INSERT INTO Rd(Time,RSSI) VALUES(%s,%d)"
    cursor.executemany(sql,datatosql)
    conn.commit()