import datetime as dt
from typing import List
import pandas as pd
from src.services.dummyDataFetcher import DummyDataFetcher
from src.services.scadaDataFetcher import ScadaDataFetcher
from src.voltageConditionCheck.voltageBand import voltageBandRange
from src.config.appConfig import getConfig


appConfig = getConfig()
fetcher = ScadaDataFetcher(appConfig["host"], appConfig["port"])
# fetcher = DummyDataFetcher
reasonabilityLimit = 100


def checkVoltageCondition(busVolt: List, pnt: dict, startTime: dt.datetime, endTime: dt.datetime):
    overVoltage, underVoltage = voltageBandRange(pnt['voltLvl'])
    indexPos = -1
    recommendation = ''
    isRecommendation = False
    isOverVoltage = False
    isUnderVoltage = False
    if busVolt:
        for temp in range(len(busVolt)-2):
            if (busVolt[temp] > overVoltage) and (busVolt[temp+1] > overVoltage) and (busVolt[temp+2] > overVoltage):
                # fetch line reactor data if over voltage exists
                lineReactorDict = fetcher.fetchEdnaData(
                    pnt['lineReactorId'], startTime, endTime)
                indexPos = temp+2
                isOverVoltage = True
                break
            if (busVolt[temp] < underVoltage) and (busVolt[temp+1] < underVoltage) and (busVolt[temp+2] < underVoltage):
                # fetch line reactor data if under voltage exists
                lineReactorDict = fetcher.fetchEdnaData(
                    pnt['lineReactorId'], startTime, endTime)
                indexPos = temp+2
                isUnderVoltage = True
                break
    # Over Voltage Condition
    if isOverVoltage:
        lineReactorData = {}
        for lineData in lineReactorDict:
            if len(lineReactorDict[lineData]):
                lineReactorData[lineData] = lineReactorDict[lineData]

        # check if any line reactor was out of service at the time of high voltage, if yes then take that in service
        for temp in lineReactorData:
            if lineReactorData[temp][indexPos] == 0:
                recommendation = "Take Suitable Line Reactor in service"
                isRecommendation = True
                print("Line {0} & recommendation, {1}". format(
                    pnt['SubStation'], recommendation))
                return indexPos, recommendation, isRecommendation

        # fetch bus reactor data
        busReactorDict = fetcher.fetchEdnaData(
            pnt['busReactorId'], startTime, endTime)
        busReactorData = {}
        for busData in busReactorDict:
            if len(busReactorDict[busData]):
                busReactorData[busData] = busReactorDict[busData]

        # if no line reactor Id or bus reactor Id is available then return no reactor availabe
        if not (len(pnt['lineReactorId']) or len(pnt['busReactorId'])):
            recommendation = "No Reactor Available"
            isRecommendation = False
            return indexPos, recommendation, isRecommendation

        # if data of no bus reactor or line reactor is available then return no reactors availabe
        if not (len(lineReactorData) and len(busReactorData)):
            recommendation = "Data of no reactor is available"
            isRecommendation = False
            return indexPos, recommendation, isRecommendation

        # check if any bus reactor is out of service at the time of high voltage
        for temp in busReactorData:
            if busReactorData[temp][indexPos] == 0:
                recommendation = "Take Suitable Bus Reactor in service"
                isRecommendation = True
                print("Line {0} & recommendation, {1}". format(
                    pnt['SubStation'], recommendation))
                return indexPos, recommendation, isRecommendation
        # no bus reactor is out of service
        recommendation = "No recommendation: All Bus Reactors are already in service"
        isRecommendation = False
        return indexPos, recommendation, isRecommendation

    # Under Voltage Condition
    if isUnderVoltage:
        busReactorDict = fetcher.fetchEdnaData(
            pnt['busReactorId'], startTime, endTime)
        busReactorData = {}
        for busData in busReactorDict:
            if len(busReactorDict[busData]):
                busReactorData[busData] = busReactorDict[busData]

        # if no bus reactor Id or line reactor Id is available then return no reactor availabe
        if not (len(pnt['lineReactorId']) or len(pnt['busReactorId'])):
            recommendation = "No Reactor Available"
            isRecommendation = False
            return indexPos, recommendation, isRecommendation
        
        # check if any bus reactor was in service at the time of low voltage, if yes then take that out of service
        for temp in busReactorData:
            if busReactorData[temp][indexPos] != 0:
                recommendation = "Take Suitable Bus Reactor out of service"
                isRecommendation = True
                print("Line {0} & recommendation, {1}". format(
                    pnt['SubStation'], recommendation))
                return indexPos, recommendation, isRecommendation
            
        # filter out line data from line dict
        lineReactorData = {}
        for lineData in lineReactorDict:
            if len(lineReactorDict[lineData]):
                lineReactorData[lineData] = lineReactorDict[lineData]

        # if data of no bus reactor or line reactor is available then return no reactors availabe
        if not (len(lineReactorData) and len(busReactorData)):
            recommendation = "Data of no reactor is available"
            isRecommendation = False
            return indexPos, recommendation, isRecommendation

        for temp in lineReactorData:
            if lineReactorData[temp][indexPos] != 0:
                recommendation = "Take Suitable Line Reactor out of service"
                isRecommendation = True
                print("Line {0} & recommendation, {1}". format(
                    pnt['SubStation'], recommendation))
                return indexPos, recommendation, isRecommendation

        # no bus reactor is out of service
        recommendation = "No recommendation: All Bus Reactors are already out of service"
        isRecommendation = False
        return indexPos, recommendation, isRecommendation
    
    return indexPos, recommendation, isRecommendation
