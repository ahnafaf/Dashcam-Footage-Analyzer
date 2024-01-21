# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:52:19 2023

@author: ahnaf
"""
import os
from datetime import datetime
from datetime import timedelta

ridesVideos = {}
listofFiles = os.listdir('D:\dashcam\Front')

# Returns a date object
def dateObject(name):
    stripped_time = name[2:15] 
    objdate = datetime.strptime(stripped_time, '%Y%m%d-%H%M')
    return objdate

