import datetime as dt
from typing import List
import pandas as pd
from src.services.dummyDataFetcher import DummyDataFetcher
from src.voltageConditionCheck.voltageBand import voltageBandRange


fetcher = DummyDataFetcher
reasonabilityLimit = 100
def checkVoltageCondition(busVolt: List, pnt: dict, startTime: dt.datetime, endTime: dt.datetime):
    overVoltage, underVoltage = voltageBandRange(pnt['voltLvl'])
    # busVolt = []
    indexPos = -1
    recommendation = ''
    isOverVoltage = False
    isUnderVoltage = False
    # for res in resDict:
    #     temp = resDict[res]
    #     if not any(x <= reasonabilityLimit for x in temp):
    #         busVolt = temp
    #         break
    if busVolt:
        for temp in range(len(busVolt)-2):
            if (busVolt[temp] > overVoltage) and (busVolt[temp+1] > overVoltage) and (busVolt[temp+2] > overVoltage):
                # fetch line reactor data if over voltage exists
                lineReactorDict = fetcher.fetchPntsData(pnt['lineReactorId'], startTime, endTime)
                indexPos = temp+2
                isOverVoltage = True
                break
            if (busVolt[temp] < underVoltage) and (busVolt[temp+1] < underVoltage) and (busVolt[temp+2] < underVoltage):
                # fetch line reactor data if under voltage exists
                lineReactorDict = fetcher.fetchPntsData(pnt['lineReactorId'], startTime, endTime)
                indexPos = temp+2
                isUnderVoltage = True
                break
    if isOverVoltage:
        
        lineReactorData = {}
        for lineData in lineReactorDict:
            if len(lineReactorDict[lineData]):
                lineReactorData[lineData] = lineReactorDict[lineData]
        lineReactorCtr = 0
        for temp in lineReactorData:
            if lineReactorData[temp][indexPos] == 0:
                recommendation = "Take Line Reactor in service"

                print("Line {0} & recommendation, {1}". format(pnt['SubStation'], recommendation))
                # push timestamp, substation_name, recommendation,voltage
                
                return indexPos, recommendation
            lineReactorCtr += 1

        if (lineReactorCtr == len(lineReactorData)) or len(pnt['lineReactorId']):
            
            # fetch us reactor data
            busReactorDict = fetcher.fetchPntsData(pnt['busReactorId'], startTime, endTime)
            busReactorData = {}
            for busData in busReactorDict:
                if len(busReactorDict[busData]):
                    busReactorData[busData] = busReactorDict[busData]
            if not (len(pnt['lineReactorId']) or len(pnt['busReactorId'])):
                recommendation = "No reactors available"
                return indexPos, recommendation
            for temp in busReactorData:
                if busReactorData[temp][indexPos] == 0:
                    recommendation = "Take Bus Reactor in service"
                    print("Line {0} & recommendation, {1}". format(pnt['SubStation'], recommendation))
                elif busReactorData[temp][indexPos] != 0:
                    recommendation = "No recommendation: All Bus Reactors are in service"
                    print("Line {0} & recommendation, {1}". format(pnt['SubStation'], recommendation))
                    
                    return indexPos, recommendation
        return indexPos, recommendation
    
    # if isUnderVoltage:
    #     lineReactorData = {}
    #     for lineData in lineReactorDict:
    #         if len(lineReactorDict[lineData]):
    #             lineReactorData[lineData] = lineReactorDict[lineData] 
    #     pass
    
    if isUnderVoltage:
            busReactorDict = fetcher.fetchPntsData(pnt['busReactorId'], startTime, endTime)
            busReactorData = {}
            for busData in busReactorDict:
                if len(busReactorDict[busData]):
                    busReactorData[busData] = busReactorDict[busData]
            if not (len(pnt['lineReactorId']) or len(pnt['busReactorId'])):
                recommendation = "No reactors available"
                return indexPos, recommendation
            lineReactorCtr = 0
            for temp in busReactorData:
                if busReactorData[temp][indexPos] != 0:
                    recommendation = "Take Suitable Bus Reactor out of service"
                    print("Line {0} & recommendation, {1}". format(pnt['SubStation'], recommendation))
                    
                    return indexPos, recommendation
                lineReactorCtr += 1

            if (lineReactorCtr == len(busReactorData)) or len(pnt['busReactorId']):
                # fetch us reactor data
                #lineReactorDict = fetcher.fetchPntsData(pnt['busReactorId'], startTime, endTime)
                lineReactorData = {}
                for lineData in lineReactorDict:
                    if len(lineReactorDict[lineData]):
                        lineReactorData[lineData] = lineReactorDict[lineData]
                for temp in lineReactorData:
                    if lineReactorData[temp][indexPos] != 0:
                        
                        recommendation = "Take Suitable Line Reactor out of service"
                        print("Line {0} & recommendation, {1}". format(pnt['SubStation'], recommendation))
                        
                        return indexPos, recommendation
                    elif lineReactorData[temp][indexPos] == 0:
                        recommendation = "No recommendation : All reactors are in service"
                        print("Line{0} & recommendation, {1}".format(pnt['Substation'], recommendation))
                        
                        return indexPos, recommendation
            return indexPos, recommendation
    # if isUnderVoltage:
    #     lineReactorData = {}
    #     for lineData in lineReactorDict:
    #         if len(lineReactorDict[lineData]):
    #             lineReactorData[lineData] = lineReactorDict[lineData] 
    #     pass

    return indexPos, recommendation
