# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 18:29:12 2020

@author: 葉幸哲
"""

### 1. Write the code to open all the data in which the file can be read and written.
##>>

fo1= open("test_data.txt", "w+") 
fo2= open("test_label.txt", "w+") 
fo3= open("train_data.txt", "w+") 
fo4= open("train_label.txt", "w+") 
# root = open("C:\Users\USER\.spyder-py3\HW4\")

### 2. Combine all the data in one data named ‘data’ in the following form:
###     [train_data     train _label     test_data      test_label   ]
##>>

data_list = []

for data in data_list:  # 從data物件讀取資料
    data_list += [data] # 把新資料加到資料組最後面
    
import os
meragefiledir = os.getcwd()+'\\MerageFiles'
filenames=os.listdir(meragefiledir)
file=open('result.txt','w')