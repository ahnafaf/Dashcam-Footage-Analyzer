# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:26:44 2023

@author: ahnaf
"""
import sqlTableJuan
import os
import psycopg2
from common_functions import *
from dotenv import load_dotenv

# List that contains [(Date, Ride No., FileName), ...]
# {Date : [FILES],[]}
# Rewritten on 30/6/23

footage_path, local_path = getPath()
listofFiles = os.listdir(footage_path)

final_dict = {}

def finalDict() -> dict:
    return sqlTableJuan.makeFinalDict(listofFiles)

final_dict = finalDict()

def insert(date, filename: str, table_name: str, curr) -> None:
    query = """
        INSERT INTO {} (date, files)
        VALUES (%s, %s);
        """.format(table_name)
    curr.execute(query, (date, filename))



def add_to_table(final_dict: dict, table_name) -> None:
    conn = connectDB()
    curr = conn.cursor()
    for key, value in final_dict.items():
        for file_list in value:
            insert(key, file_list, table_name, curr)
    conn.commit()
    curr.close()
    conn.close()

add_to_table(final_dict, "ride_date_file")