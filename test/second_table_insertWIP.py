# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 21:48:26 2023

@author: ahnaf
"""

import psycopg2
import computVision
from common_functions import *
import table3_helper
from geopy.distance import geodesic

footage_path, local_path = getPath()


def dms_to_dd(coord_str):
    direction = coord_str[0]  # Extract the direction (N, S, E, W)
    degrees = float(coord_str[1:])  # Extract the numeric degrees part
    dd = degrees if direction in [
        'N', 'E'] else -degrees  # Adjust for direction
    return dd


def remove_far_points(latitude, longitude, threshold):
    if not latitude or not longitude:
        return [], []

    new_latitude = [latitude[0]]
    new_longitude = [longitude[0]]
    last_coords = (latitude[0], longitude[0])

    for lat, lon in zip(latitude[1:], longitude[1:]):
        distance = geodesic((lat, lon), last_coords).meters
        if distance <= threshold:
            new_latitude.append(lat)
            new_longitude.append(lon)
            last_coords = (lat, lon)

    return new_latitude, new_longitude


def fetchData():
    conn = connectDB()
    curr = conn.cursor()
    curr.execute('''SELECT * FROM ride_date_file;''')
    for id, date, file in curr.fetchall():
        speed = []
        longitude = []
        latitude = []
        timestamp = []
        last_coords = None
        file_list = convertList(file)
        for file_name in file_list:
            list_of_coords = computVision.readCoords(file_name)
            print(f"Processing: {file_name}")
            for infoDict in list_of_coords:
                speed_value = int(infoDict['Speed'].strip("km/h"))
                longitude_value = table3_helper.convertCords(
                    infoDict['Longitude'])
                latitude_value = table3_helper.convertCords(
                    infoDict['Latitude'])
                timestamp_value = infoDict['timestamp']

                if last_coords is not None:
                    # Calculate distance between current and previous coordinates
                    distance = geodesic(
                        (latitude_value, longitude_value), last_coords).meters
                    # If the distance is greater than the threshold, skip adding the data points
                    if distance > 500:
                        continue
                    else:
                        # Update last_coords to the current coordinates if they are within the threshold
                        last_coords = (latitude_value, longitude_value)
                else:
                    # If it's the first iteration, set last_coords to the current coordinates
                    last_coords = (latitude_value, longitude_value)
                # Append the data points when they meet the threshold condition
                # print(longitude, latitude)
                speed.append(speed_value)
                longitude.append(longitude_value)
                latitude.append(latitude_value)
                timestamp.append(timestamp_value)
        insert(date, timestamp, latitude, longitude, speed, "rides_data", curr)
    conn.commit()
    curr.close()
    conn.close()


def insert(date, timestamp, latitude: str, longitude: str, speed, table_name: str, curr) -> None:
    query = """
        INSERT INTO {} (date, timestamp, longitude, latitude, speed)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
        """.format(table_name)
    curr.execute(query, (date, timestamp, longitude, latitude, speed))


def convertList(sqlList):  # Not needed to be called
    return sqlList.rstrip('}').lstrip('{').split(',')


def fillTable():  # Not needed to be called explicitly
    conn = connectDB()
    curr = conn.cursor()
    curr.execute('''SELECT ride_date_file.files, rides_data.date, rides_data.ride_id
                FROM ride_date_file
                JOIN rides_data
                ON ride_date_file.date = rides_data.date
                AND ride_date_file.ride = rides_data.ride_id
                WHERE cardinality(rides_data.timestamp) = 0;
                ''')
    for files, date, ride_id in curr.fetchall():
        print(files)


fetchData()
