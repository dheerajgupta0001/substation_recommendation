import datetime as dt
from typing import List
import psycopg2
from src.typeDefs.fetchPnt import FetchPnt
from src.services.dummyDataFetcher import DummyDataFetcher

conn = psycopg2.connect(
    dbname="TestDB",
    user="aryanbhat",
    password="aryanbhat",
    host="localhost",
    port="5432"
)

# Create a cursor object using the connection
cur = conn.cursor()
databaseLimit = 1000


def insertToDB(time_stamp:dt.datetime, substation:str, recommendation:str, busVolt: list):
    cur.execute('INSERT INTO "Latest_Recommendation" (timestamp, substation_name, recommendation,voltage) VALUES (%s, %s, %s, %s)', (time_stamp, substation, recommendation, busVolt))
    cur.execute('INSERT INTO "Recommendation_History" (timestamp, substation_name, recommendation,voltage) VALUES (%s, %s, %s, %s)', (time_stamp, substation, recommendation, busVolt))
    conn.commit()
    return True