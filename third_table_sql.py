# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 02:18:21 2023

@author: ahnaf
"""

# Table 3, first making the coordinates
# '''SELECT * FROM rides_data WHERE ride_id = 1 AND date = '2023-06-16';''' IGNORE

import os
import numpy as np
from datetime import *
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from common_functions import *
from table3_helper import *
from geopy.distance import geodesic

footage_path, local_path = getPath()
mapBoxKey = os.getenv('mapKey')

def convertList(sqlList): # Not needed to be called
    return sqlList.rstrip('}').lstrip('{').split(',')

def fetchData():
    def convertCoordinates(latitude, longitude):
        latitude = convertList(latitude)
        longitude = convertList(longitude)
        return latitude, longitude
    conn = connectDB()
    curr = conn.cursor()
    curr.execute('''SELECT * FROM rides_data;''') # ID = 1 FOR TESTING PURPOSES! REMOVE!
    for id,date,timestamp,longitude,latitude,speed in curr.fetchall():
        end_loc = ""
        start_loc = ""
        # Loops through, speed is outputted as a single list. Need parallel for loops.
        latitude, longitude = convertCoordinates(latitude,longitude)
        print(f"Processing date: {date}")
        distance = getDistance(timestamp, speed)
        hard_starts, hard_accls = hardMovement(timestamp, speed)
        if len(latitude) > 2 or len(longitude) > 2:
            start_loc = getLocationName(float(latitude[0]),float(longitude[0]))
            end_loc = getLocationName(float(latitude[-1]),float(longitude[-1]))
        durations = duration(timestamp)
        fuel_used, fuel_price = fuelCost(distance, 30, 2.97)
        insert(date, distance, hard_starts, hard_accls, str(start_loc), str(end_loc), durations, fuel_price, "stats_table", curr)
        #makeGraphplotLy(timestamp,speed, "derivative")
    conn.commit()
    curr.close()
    conn.close()

def insert(date, distance_travelled, hs, ha, start_l, end_l, duration, fuel_cost, table_name: str, curr) -> None:
    query = """
        INSERT INTO {} (date, distance_travelled, hard_stops, hard_accls, start_loc, end_loc, duration, fuel_cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
        """.format(table_name)
    curr.execute(query, (date, distance_travelled, hs, ha, start_l, end_l, duration, fuel_cost))

fetchData()