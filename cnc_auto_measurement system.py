from threading import Thread as thread
from adxl345 import ADXL345
import time
import pymssql
from collections import Iterable
from grove.adc import ADC
import pandas as pd
import numpy as np
import math
import sys
import grove.i2c
#########################################SQL CONNECTION###########################################################################################
server = '140.118.199.95'
user = 'sa'
password = '789'
database = 'DataFromCNC'
port = '1433'
conn = pymssql.connect(server,user,password,database,port)
cursor = conn.cursor(as_dict=True)
##########################################grove sound library#####################################################################################
__all__ = ['GroveSoundSensor']
class GroveSoundSensor(object):
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
    @property
    def sound(self):
        value = self.adc.read(self.channel)
        return value
        Grove = GroveSoundSensor
##########################################ADC library##############################################################################################
__all__ = [
    "ADC",
    "RPI_HAT_NAME", "RPI_ZERO_HAT_NAME",
    "RPI_HAT_PID", "RPI_ZERO_HAT_PID"
]
RPI_HAT_PID      = 0x0004
RPI_ZERO_HAT_PID = 0x0005
RPI_HAT_NAME     = 'Grove Base Hat RPi'
RPI_ZERO_HAT_NAME= 'Grove Base Hat RPi Zero'
class ADC(object):
    def __init__(self, address = 0x04):
        self.address = address
        self.bus = grove.i2c.Bus()
    def read_raw(self, channel):
        addr = 0x10 + channel
        return self.read_register(addr)
    def read_voltage(self, channel):
        addr = 0x20 + channel
        return self.read_register(addr)
    def read(self, channel):
        addr = 0x30 + channel
        return self.read_register(addr)
    @property
    def name(self):
        id = self.read_register(0x0)
        if id == RPI_HAT_PID:
            return RPI_HAT_NAME
        elif id == RPI_ZERO_HAT_PID:
            return RPI_ZERO_HAT_NAME
    @property
    def version(self):
        return self.read_register(0x3)
    def read_register(self, n):
        try:
            self.bus.write_byte(self.address, n)
            return self.bus.read_word_data(self.address, n)
        except IOError:
            print("Check whether I2C enabled and   {}  or  {}  inserted".format \
                    (RPI_HAT_NAME, RPI_ZERO_HAT_NAME))
            sys.exit(2)
            return 0
########################################Three TASKS###############################################################################################
###Vibration######################################################################################################################################
def Vibration():
    count1 = 0 #count為記錄存檔的數數
    while True:
        count1 += 1
        adxl345 = ADXL345() #引進加速規的library
        adxl345.set_bandwidth_rate(0x0B)  #ADXL345的頻寬設定
        k = 0   #k為紀錄加速規完成了幾秒的變數
        DATA = [[]]  #DATA定義存放五分鐘的EXCEL資料空間
        while True:
            i = 0   #i定義每秒加速規的取樣頻率
            k +=1
            Data = [[]]  #Data為暫存一秒內的所有RAW DATA
            X = []  #X軸的儲存空間
            Y = []  #Y軸的儲存空間
            Z = []  #Z軸的儲存空間
            Time = []   #RAW DATA時間的儲存空間
            starttime = time.time()     #紀錄每一秒資料的起始時間
            while True:
                i += 1
                axes = adxl345.get_axes()  #取得加速規的RAW DATA來源
                X = [axes['x']]  #取得X軸訊號
                Y = [axes['y']]  #取得Y軸訊號
                Z = [axes['z']]  #取得Z軸訊號
                Data += [[time.ctime(time.time()),axes['x'],axes['y'],axes['z']]]  #將每一次的RAW DATA暫存到名為Data的空間
                Time += time.ctime(time.time()) #將每一次的時間轉換為實際時間並存在Time的暫存空間
                if time.time()-starttime >=1:break   #每一秒將停止迴圈並進行到下一個迴圈
            #print('sampling rate for vibration',i)
            print('Vibration complete:',k) #顯示目前已經到第幾秒的資料
            np_X = np.array(X)  #將XYZ三軸的數據進行轉換，目的為了取得每一個矩陣裡的最大值
            np_Y = np.array(Y)
            np_Z = np.array(Z)
            global x,y,z    #回傳每軸每一秒的最大值，將提供給名為SQL的function進行SQL上船動作
            x = round(max(np.abs(np_X)),2)   #取得最大值，並四捨五入進去小數第二位
            y = round(max(np.abs(np_Y)),2)
            z = round(max(np.abs(np_Z)),2)
            DATA += Data  #將每一秒的RAW DATA暫存起來  等到到五分鐘的時候存成一個EXCEL檔案
            #return x,y,z
            if k>299 : break
        filename = '/home/pi/ID4C/demo_data/vibration/demo for vibration' + str(count1)     #EXCEL檔案的存檔格式
        dataframe = pd.DataFrame(DATA)
        dataframe.to_csv(filename,sep=',')
        #print('Vibration_Complete'+str(count))
###Sound##########################################################################################################################################
def Sound():
    from grove.helper import SlotHelper #引進LIBRARRY
    sh =  SlotHelper(SlotHelper.ADC)
    #pin = sh.argv2pin()
    sensor = GroveSoundSensor(0)  #後面括號為raspberry pi 的I2C腳位
    count2 = 0
    while True:
        count2 +=1
        k = 0
        DATA = [[]]
        while True:
            i = 0
            Data = [[]]
            Sound = []
            Time = []
            k +=1
            starttime = time.time()
            while True:
                i += 1
                db = 94+20*math.log(float(sensor.sound+50)/3160)    #分貝轉換公式
                Sound += [db]
                Time += time.ctime(time.time())
                Data += [[time.ctime(time.time()),db]]
                if time.time()-starttime >= 1: break
            #print('sampling rate for sound:',i)
            print('Sound complete',k)
            np_S = np.array(Sound)
            global s
            s = round(max(np.abs(np_S)),2)
            DATA += Data
            #return s
            if k>299 : break
    
        filename = '/home/pi/ID4C/demo_data/sound/demo for sound'+str(count2)
        dataframe = pd.DataFrame(DATA)
        dataframe.to_csv(filename,sep=',')
        #print('Sound_Complete'+str(count))
###Current########################################################################################################################################
def Current():
    adc = ADC()  #ADC轉換library
    count3 = 0
    while True: 
        k = 0
        count3 += 1
        DATA = [[]]
        while True:
            i = 0
            Data = [[]]
            Current = []
            Time = []
            k += 1
            starttime = time.time()
            while True:
                i += 1
                Current += [float(adc.read_voltage(2)-3000)/165]                   #電流轉換公式(待修正)
                Data += [[time.ctime(time.time()),float(adc.read_voltage(0))/50]]
                #Data += [[time.ctime(time.time()),float(adc.read_voltage(0))/50]
                if time.time()-starttime>=1:break
                #if time.time() - starttime >=1 :break
            #print('sampling rate for current',i)
            print('Current complete',k)
            np_C = np.array(Current)
            global c
            c = round(max(np.abs(np_C)),2)
            DATA += Data
            #return c
            if k>299 : break

        filename = '/home/pi/ID4C/demo_data/current/demo for current'+str(count3)
        dataframe = pd.DataFrame(DATA)
        dataframe.to_csv(filename,sep=',')
        #print('Current_Complete'+str(count))
###################SQL UPLOAD######################################################################################################################
def SQL():
    time.sleep(30)     #先讓程式跑一陣子，以避免SQL這個function找不到全域變數
    while True:
        s1 = time.time()  #紀錄起始時間 
        time.sleep(0.8)     #每秒傳一次數值
        t = time.localtime(time.time())  #進行時間格式的轉檔，為了配合labview
        Time = time.strftime("%y/%m/%d_%H:%M:%S",t)  #進行時間格式的轉檔，為了配合labview
        datatosql=[(Time,x,y,z,s,c)] #每秒要上傳的資料
        print(datatosql)
        sql = 'INSERT INTO CNC(Time,V_x,V_y,V_z,Sound,SpindleCurrent) VALUES(%s,%d,%d,%d,%d,%d)'    #建立SQL語法
        cursor.executemany(sql,datatosql)   #執行SQL語法
        conn.commit()  #關閉SQL連接
        print('complete')   #確認每一秒的讀值已完成
        print(time.time()-s1)   #紀錄每一次動作的時間
####################Threading Four Tasks###########################################################################################################


#為了平行執行這四個function,使用Threading多執行緒讓多個function同時運行同時處理
thread(target=Vibration).start()
thread(target=Sound).start()
thread(target=Current).start()
thread(target=SQL).start()


##################Test by return values###########################################################################################################


#先前為了測試不要用global variable，使用return的方法
#優:較為穩定,上傳的時間間隔較固定
#缺:時間執行過慢
#可能的解決方案: 在linux環境下下載numba這個library,可以加速執行，減少處理時間


#while True:
#       thread(target=Vibration).start()
#       thread(target=Sound).start()
#       thread(target=Current).start()
#       #time.sleep(1)
#       t1 = time.time()
#       v_x = Vibration()[0]
#       v_y = Vibration()[1]
#       v_z = Vibration()[2]
#       #t2 = time.time()
#       t = time.localtime(time.time())
#       #t3 = time.time()
#       Time = time.strftime("%Y/%m/%d_%H:%M:%S",t)
#       #t4 = time.time()
#       datatosql = [(Time,v_x,v_y,v_z,Sound(),Current())]
#       #t5 = time.time()
#       sql = 'INSERT INTO CNC(Time,V_x,V_y,V_z,Sound,SpindleCurrent) VALUES(%s,%d,%d,%d,%d,%d) '
#       cursor.executemany(sql,datatosql)
#       conn.commit()
#       print('complete')
#       print(time.time()-t1)
