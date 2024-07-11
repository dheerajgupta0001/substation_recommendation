from src.config.appConfig import getConfig, getPnts
from src.loggerFactory import initFileLogger
from src.services.scadaDataFetcher import ScadaDataFetcher
# from src.services.dummyDataFetcher import DummyDataFetcher
from src.voltageConditionCheck.checkVoltage import checkVoltageCondition
import datetime as dt
from src.utils.reasonabilityCheck import getReasonableVoltVals
from src.repos.recommendation import insertRecomToHistory, deleteFromDraftDB, getOpenRecomId, updateHREndTimeDB, updateLatestRecoms, markRecomsAsClosed
import pandas as pd
import time

# databaseLimit = 10000

# for logs
logger = initFileLogger("app_logger", "app_logs/app_log.log", 50, 10)

logger.info("started reading config File script")
appConfig = getConfig()
pntsConfig = getPnts()
fetcher = ScadaDataFetcher(appConfig["host"], appConfig["port"])

endTime = dt.datetime.now()
startTime = endTime - dt.timedelta(minutes=5)
# startTime = dt.datetime(2024, 5, 20, 6, 0)
# endTime = dt.datetime(2024, 5, 20, 12, 0)

# time.sleep(1)
latestRecommendation = []
for substationConf in pntsConfig:
    # fetch the buses voltages of the substation
    resDict = fetcher.fetchEdnaData(
        substationConf['voltId'], startTime, endTime)

    # fetcher = DummyDataFetcher
    # resDict = fetcher.fetchPntsData(pnt['voltId'], startTime, endTime)
    # remove dummy line data

    substationBusesVoltages: dict[str, list[float]] = {}
    # discard points with no values from the dictionary
    for res in resDict:
        if len(resDict[res]):
            substationBusesVoltages[res] = resDict[res]

    # get reasonable bus voltage values for analysis
    busVolts = getReasonableVoltVals(substationBusesVoltages)

    isSuccess = False
    voltSamplInd, recommendation, isRecommendation = checkVoltageCondition(
        busVolts, substationConf, startTime, endTime)
    if voltSamplInd != -1:
        time_stamp = startTime + dt.timedelta(minutes=voltSamplInd)
        subStationName = substationConf['SubStation']
        if len(busVolts) > 0:
            busVolts = ['%.2f' % elem for elem in busVolts]

        busVoltsStr = ','.join([str(elem) for elem in busVolts])
        openRecomId = getOpenRecomId(subStationName, recommendation)
        isSuccess = insertRecomToHistory(time_stamp, subStationName,
                                         recommendation, busVoltsStr, isRecommendation, openRecomId, startTime)
        # time.sleep(1)
        if isSuccess:
            print("Insertion to database successful")
        else:
            print("Insertion to database failed")
        latestRecommendation.append(subStationName)

# deleteFromDraftDB(startTime)
# updateHREndTimeDB(startTime, latestRecommendation)
isSuccess = markRecomsAsClosed(startTime)
isSuccess = updateLatestRecoms()
