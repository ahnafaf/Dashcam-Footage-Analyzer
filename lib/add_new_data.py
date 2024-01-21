# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 20:50:10 2023

@author: ahnaf
"""
# Process new files

import os
import psycopg2
import sqlTableJuan
import first_table_creator
from dotenv import load_dotenv

path = "D:\dashcam\Front"

def connectDB():
    conn = psycopg2.connect(
        host="localhost",
        database="python_car",
        user="ahnaf",
        password="123"
        )
    return conn

def convertList(sqlList): # Not needed to be called
    return sqlList.rstrip('}').lstrip('{').split(',')

def makeSet():
    set_of_files = set()
    conn = connectDB()
    curr = conn.cursor()
    curr.execute('''SELECT files FROM ride_date_file;''')
    sql_file_list = curr.fetchall()
    for indiv_file_list in sql_file_list:
        for file in indiv_file_list:
            converted = convertList(file)
            for i in converted:
                set_of_files.add(i) 
    return set_of_files

def directorySet(path):
    return set(os.listdir(path))

def setDiff(files_directory, sql_set):
    # Returns the files that are inside the folder but not SQL
    return files_directory - sql_set

def processor():
    # Makes the final dict for the difference set
    list_of_diff = list(setDiff(directorySet(path), makeSet()))
    dict_of_diff = sqlTableJuan.makeFinalDict(list_of_diff)
    first_table_creator.add_to_table(dict_of_diff, "ride_date_file")

    
print(directorySet(path))