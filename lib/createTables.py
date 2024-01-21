# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 17:15:14 2023

@author: ahnaf
"""

# SQL Table creator! Run this if you don't have the SQL tables!
# If you cannot create table, run this using query tool: 
# GRANT CREATE ON SCHEMA public TO my_database_user;

import psycopg2

def connectDB():
    conn = psycopg2.connect(
        host="localhost",
        database="python_car",
        user="ahnaf",
        password="123"
        )
    return conn

def createDataTable():
    conn = connectDB()
    curr = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS rides_data (
    id SERIAL PRIMARY KEY,
	date date NOT NULL,
	timestamp TIMESTAMP ARRAY NOT NULL,
	longitude TEXT NOT NULL,
	latitude TEXT NOT NULL,
	speed integer[]
    );"""
    curr.execute(query)
    conn.commit()

def createRideTable():
    conn = connectDB()
    curr = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS ride_date_file(
            id SERIAL PRIMARY KEY,
            date date NOT NULL,
            files text NOT NULL);"""
    curr.execute(query)
    conn.commit()
    
def createThirdTable():
    conn = connectDB()
    curr = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS stats_table (
    id SERIAL PRIMARY KEY,
    date DATE,
    distance_travelled FLOAT,
    hard_stops INTEGER,
    hard_accls INTEGER,
    start_loc TEXT,
    end_loc TEXT,
    duration FLOAT,
    fuel_cost FLOAT);"""
    curr.execute(query)
    conn.commit()
    
createThirdTable()
