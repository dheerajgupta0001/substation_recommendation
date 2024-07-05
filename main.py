from src.config.appConfig import getConfig, getPnts
from src.loggerFactory import initFileLogger
from src.services.scadaDataFetcher import ScadaDataFetcher
# from src.services.dummyDataFetcher import DummyDataFetcher
from src.voltageConditionCheck.checkVoltage import checkVoltageCondition
import datetime as dt
from src.utils.reasonabilityCheck import checkReasonabilityLimit
from src.repos.recommendation import insertToDB, deleteFromDraftDB
import pandas as pd
import time

databaseLimit = 10000

# for logs
logger = initFileLogger("app_logger", "app_logs/app_log.log", 50, 10)

logger.info("started reading config File script")
appConfig = getConfig()
pntsConfig = getPnts()

endTime = dt.datetime.now()
# startTime = dt.datetime(2024, 5, 20, 6, 0)
# endTime = dt.datetime(2024, 5, 20, 12, 0)
startTime = endTime - dt.timedelta(minutes=15)

# time.sleep(1)
for pnt in pntsConfig:
    fetcher = ScadaDataFetcher(appConfig["host"], appConfig["port"])
    resDict = fetcher.fetchEdnaData(
        pnt['voltId'], startTime, endTime)
    # fetch voltage data from excel
    recommendation = False
    # fetcher = DummyDataFetcher
    # resDict = fetcher.fetchPntsData(pnt['voltId'], startTime, endTime)
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
    indexPos, recommendation, isRecommendation = checkVoltageCondition(
        busVolt, pnt, startTime, endTime)
    if indexPos != -1:
        # if not recommendation:
        #     recommendation = ""
        time_stamp = startTime + dt.timedelta(minutes=indexPos)
        subStationName = pnt['SubStation']
        if len(busVolt):
            busVolt = ['%.2f' % elem for elem in busVolt]
            
        busVolt = ','.join([str(elem) for elem in busVolt])
        isSuccess = insertToDB(time_stamp, subStationName,
                               recommendation, busVolt, isRecommendation)
        time.sleep(1)
        # insertion to database only one time

        if isSuccess:
            print("Insertion to database successful")

        else:
            print("Insertion to database failed")

deleteFromDraftDB(startTime)
