import os
from datetime import datetime
from datetime import timedelta
import json
from common_functions import *
from dotenv import load_dotenv

footage_path, local_path = getPath()
file_list = os.listdir(footage_path)


def makeDict(file_list) -> dict:
    date_obj_list = []
    final_dict ={}
    for i in file_list:
        date_obj_list.append(dateObject(i).date())
    for i in range(len(date_obj_list)):
        if date_obj_list[i] in final_dict:
            final_dict[date_obj_list[i]].append(file_list[i])
        else:
            final_dict[date_obj_list[i]] = [file_list[i]]
    return final_dict

# Takes a list of timestamps of dashcam videos and calculates number of rides
def listRideSeperator(dictofVids: dict) -> dict:
    new_dict = {}
    for date,fileList in dictofVids.items():# Outside loop, goes through DATE: [LIST]
        date_list = [[]]
        counter = 0
        date_list[0].append(fileList[0])
        for index in range(1,len(fileList)): # Accesses the file list,
            if dateObject(fileList[index]) - dateObject(fileList[index-1]) >= timedelta(minutes= 4):
                counter += 1
                date_list.append([fileList[index]])
            else:
                date_list[counter].append(fileList[index])
        new_dict[date] = date_list
    return new_dict

def makeFinalDict(file_list):
    final_dict = makeDict(file_list)
    final_dict = listRideSeperator(final_dict)
    return final_dict
