# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:52:19 2023

@author: ahnaf
"""
import os
from datetime import datetime
from datetime import timedelta
import psycopg2
import pandas as pd


ridesVideos = {}
listofFiles = os.listdir('C:/Users/ahnaf/Videos/dashcam funny/Front')
setofDay = set()
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Returns a date object
def dateObject(name):
    stripped_time = name[2:15]
    objdate = datetime.strptime(stripped_time, '%Y%m%d-%H%M%S')
    return objdate


# Make the set of listofFiles, set contains the day.
def setMaker():
    for i in listofFiles:
        objdate = dateObject(i)
        day_of_week = objdate.weekday()
        setofDay.add(day_of_week)

## Creates the connection to Postgres DB
def create_conn():
    conn = psycopg2.connect(
        host="localhost",
        database="python_car",
        user="",
        password="123"
    )
    return conn


print(create_conn())