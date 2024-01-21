# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 17:09:26 2023

@author: ahnaf
"""

# First test to connect with SQL database and upload the date
# the ride and the files

import os
import psycopg2
#import regular_exp
#import rideIncrement
import datetime
from datetime import date
import pandas as pd
from dotenv import load_dotenv

# Connects to database, and then establishes a cursor
conn = psycopg2.connect(
    host="localhost",
    database="python_car",
    user="ahnaf",
    password="123"
    )
curr = conn.cursor()

print(conn)
# Inserts into the table
def insert(ride: int, date, filename: str, table_name: str) -> None:
    curr.execute("""
        INSERT INTO table_name (ride, date, filename)
        VALUES (%s, %s, %s);
        """,
        (ride, date, filename))



conn.commit()
curr.close()
conn.close()
