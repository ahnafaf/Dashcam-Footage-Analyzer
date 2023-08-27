# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 18:45:49 2023

@author: ahnaf
"""

## RegEx

import re

def clean_string(input_string):
    # Remove spaces
    input_string = input_string.replace(" ", "")
    
    # Replace pound sign (#) with 'E' if it exists
    input_string = input_string.replace("£", "E")
    
    # Replace 'O' with '0' if it exists
    input_string = input_string.replace("O", "0")
    
    return input_string

def extract_data(input_string):
    pattern = re.compile(r'(\d+km/h)(E|N|W|S)(\d+\.\d+),(E|N|W|S)(\d+\.\d+)')
    match = pattern.match(input_string)
    
    if match:
        speed = match.group(1)
        coord1_direction = match.group(2)
        coord1 = float(match.group(3))
        coord2_direction = match.group(4)
        coord2 = float(match.group(5))
        thisdict = {
          "Speed": speed,
          "Longitude": coord1_direction + str(coord1),
          "Latitude": coord2_direction + str(coord2)
        }
        
        return thisdict
    else:
        return None

# Example 
# input_string = '43km/h £55. 3674 ,N25. 3066'
# input_string = clean_string(input_string)
# print(extract_data(input_string))
# {'Speed': '43km/h', 'Longitude': 'E55.3674', 'Latitude': 'N25.3066'}