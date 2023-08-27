## Helper functions for third table

import psycopg2 
import os
import numpy as np
from datetime import *
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from common_functions import *
from geopy.geocoders import Nominatim
import math 
from geopy.geocoders import GoogleV3
from dotenv import load_dotenv


mapBoxKey = os.getenv('mapKey')

def duration(timestamps: list):
    if len(timestamps) < 2:
        return 0
    first_datetime = timestamps[0]
    last_datetime = timestamps[-1]
    time_difference = last_datetime - first_datetime
    return time_difference.total_seconds() / 60.0

def fuelCost(kilometers: float, average_mpg: float, fuel_price) -> float:
    # 1km = 0.621371 miles
    miles = kilometers * 0.621371
    fuel_used = miles/average_mpg
    # returns fuel used in liters, fuel price, should be put as price/liter.
    return "{:.2f}".format(fuel_used*3.78541), "{:.2f}".format(fuel_used*3.78541*fuel_price)

def getLocationName(latitude, longitude):
    geolocator = GoogleV3(os.getenv('GOOGLE_KEY'))
    locations = geolocator.reverse(f"{latitude}, {longitude}")
    return locations


def makeMap(latitude,longitude,speed):
    #longitudes1 = [-74.0060, -0.1278, 2.3522, 139.759455, 151.2093]
    #latitudes1 = [40.7128, 51.5074, 48.8566, 35.682839, -33.8688]

    pio.renderers.default='browser'
    fig = go.Figure()
    # Add Scattermapbox trace for the footage_footage_path
    fig.add_trace(
        go.Scattermapbox(
            mode='lines+markers',
            lon=longitude,
            lat=latitude,
            marker=dict(size=10),
            line=dict(width=2),
            text=speed
        )
    )
    # Set the layout to display the map
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',  # Choose a map style: 'open-street-map', 'carto-positron', 'carto-darkmatter', etc.
            center=dict(lat=0, lon=0),
            accesstoken=mapBoxKey
            )
        )
    fig.show()
    
def getDistance(time_objects, speed):
    if len(time_objects) < 5 or len(speed) < 5:
        return 0
    """
    def normalGraph():     
        print("Making Graph")
        fig = go.Figure(data=go.Scatter(x=time_objects, y=speed, mode='lines+markers'))
        fig.update_layout(title='Speed vs Time',
                          xaxis_title='Time',
                          yaxis_title='Speed')
        fig.show()

    def derivative():
        timestamps = [obj.timestamp() for obj in time_objects]
        # Calculate the derivative (change in speed per second)
        speed_derivative = np.gradient(speed, timestamps)
        # Create the plotly graph for speed and time
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_objects, y=speed, mode='lines+markers', name='Speed'))
        fig.add_trace(go.Scatter(x=time_objects[1:], y=speed_derivative, mode='lines+markers', name='Speed Derivative'))
        fig.update_layout(title='Speed and Derivative vs Time',
                          xaxis_title='aTime',
                          yaxis_title='Speed / Speed Derivative')
        # print(speed_derivative)
        fig.show()
    """
    numerical_timestamps = np.array([timestamp.timestamp() for timestamp in time_objects])
    # Calculate time differences
    time_diff = np.diff(numerical_timestamps)    
    # Perform numerical integration of speed with respect to time
    distance = np.trapz(speed[:-1] * time_diff, numerical_timestamps[:-1]) / 3600  # Exclude the last value and convert to km
    return distance



def convertCords(coord_str):
    direction = coord_str[0]  # Extract the direction (N, S, E, W)
    degrees = float(coord_str[1:])  # Extract the numeric degrees part
    dd = degrees if direction in ['N', 'E'] else -degrees  # Adjust for direction
    return dd

def hardMovement(time_objects, speed):
    if len(time_objects) < 5 or len(speed) < 5:
        return 0,0
    # Uses a expotential scale to rate a movement from soft to hard, if its soft 0 is added, if its hard then 1 is added, which is equivalent to
    # 6 points lost
    def exponential_scaling_stop(stopping_rate, start_point, end_point):
        if stopping_rate >= start_point:
            # Mapping for values above or equal to start_point
            a = 1.0 / (end_point - start_point)
            b = 1 - a * end_point
            return max(0, min(1, a * stopping_rate + b))
        else:
            # Mapping for values below start_point
            a = 1.0 / (-end_point - start_point)
            b = 1 - a * start_point
            return max(0, min(1, a * stopping_rate + b))
        
    def expotential_scaling_start(stopping_rate, start_point, end_point):
        if stopping_rate <= start_point:
            # Mapping for values below or equal to start_point
            a = 1.0 / (end_point - start_point)
            b = 1 - a * end_point
            return max(0, min(1, a * stopping_rate + b))
        else:
            # Mapping for values above start_point
            a = 1.0 / (end_point - start_point)
            b = 1 - a * start_point
            return max(0, min(1, a * stopping_rate + b))
    hard_stops = 0
    hard_starts = 0
    timestamps = [obj.timestamp() for obj in time_objects]
    speed_derivative = np.gradient(speed, timestamps)
    for num in speed_derivative:
        if num <= 0:
            hard_stops += exponential_scaling_stop(num, -2, -8)
        elif num > 0:
            hard_starts += expotential_scaling_start(num, 2, 8)
        
    return hard_starts, hard_stops

from geopy.distance import geodesic

def total_distance_covered(latitude, longitude):
    coordinates = list(zip(latitude,longitude))
    total_distance = 0.0
    for i in range(len(coordinates) - 1):
        start_point = coordinates[i]
        end_point = coordinates[i + 1]
        total_distance += geodesic(start_point, end_point).kilometers
    return total_distance
