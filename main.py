from src.config.appConfig import getConfig, getPnts
from src.loggerFactory import initFileLogger
from src.services.scadaDataFetcher import ScadaDataFetcher
from src.services.dummyDataFetcher import DummyDataFetcher
from src.voltageConditionCheck.checkVoltage import checkVoltageCondition
import datetime as dt
from src.utils.reasonabilityCheck import checkReasonabilityLimit
from src.repos.recommendation import insertToDB
import pandas as pd
import psycopg2
import time

conn = psycopg2.connect(
    dbname="TestDB",
    user="aryanbhat",
    password="aryanbhat",
    host="localhost",
    port="5432"
)

# Create a cursor object using the connection
cur = conn.cursor()

databaseLimit = 10000

# for logs
logger = initFileLogger("app_logger", "app_logs/app_log.log", 50, 10)

logger.info("started reading config File script")
appConfig = getConfig()
pntsConfig = getPnts()

# endDt = dt.datetime.now()
# endDt = dt.datetime(endDt.year,endDt.month,endDt.day)
startTime = dt.datetime(2024, 5, 20, 6, 0)
endTime = dt.datetime(2024, 5, 20, 12, 0)
# endTime = dt.datetime.now()
# startTime = endTime- dt.timedelta(minutes=15)

cur.execute('DELETE FROM "Latest_Recommendation"')
conn.commit()
time.sleep(2)
for pnt in pntsConfig:
    # fetcher = ScadaDataFetcher(appConfig["host"], appConfig["port"])
    # resDict = fetcher.fetchEdnaData(
    #     pnt['Voltage'], startTime, endTime)
    # fetch voltage data from excel
    recommendation = False
    fetcher = DummyDataFetcher
    resDict = fetcher.fetchPntsData(pnt['voltId'], startTime, endTime)
    # remove dummy line data
    dataDict = {}
    for res in resDict:
        if len(resDict[res]):
            dataDict[res] = resDict[res]

    busVolt = checkReasonabilityLimit(dataDict)
    # for res in dataDict:
    # if pnt['SubStation'] == 'RAIGR_PG':
    #     print("ok")
    #     pass
    isSuccess = False
    indexPos, recommendation = checkVoltageCondition(busVolt, pnt, startTime, endTime)
    if indexPos != -1:
        time_stamp = startTime + dt.timedelta(minutes=15*indexPos)
        subStationName = pnt['SubStation']
        isSuccess =  insertToDB(time_stamp, subStationName, recommendation, busVolt)
        #insertion to database only one time
        
        if isSuccess:
            print("Insertion to database successful")
        
        else:
            print("Insertion to database failed")

    # call processing function from here and from there call for reactors data if any descrepency found

    pass
# path, voltage = processConfig(file_name , file_type, voltage_level) # type: ignore
# fetchers(path, voltage)