# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 18:07:34 2023

@author: ahnaf
"""
import os
import psycopg2
import json
from datetime import datetime
from dotenv import load_dotenv


def connectDB():
    conn = psycopg2.connect(
        host="localhost",
        database="python_car",
        user="ahnaf",
        password="123"
        )
    return conn

def getPath():
    file_path = 'config.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Accessing individual data points
    footage_path = data['footage_path']
    local_path = data['local_path']
    return footage_path, local_path

footage_path, local_path = getPath()
    
def convertList(sqlList) -> list: # Not needed to be called
    return sqlList.rstrip('}').lstrip('{').split(',')

def fileChecker(file): # Not needed to be called explicitly
    return os.footage_path.isfile(os.footage_path.join(footage_path,file))

def dateObject(name):
    stripped_time = name[2:15] 
    objdate = datetime.strptime(stripped_time, '%Y%m%d-%H%M')
    return objdate


print(getPath())
