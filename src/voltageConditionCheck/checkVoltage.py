import datetime as dt
from src.services.scadaDataFetcher import ScadaDataFetcher
from src.voltageConditionCheck.voltageBand import voltageBandRange
from src.config.appConfig import getJsonConfig


reasonabilityLimit = 100


def checkVoltageCondition(busVolts: list[float], pnt: dict, startTime: dt.datetime, endTime: dt.datetime) -> tuple[int, str, bool]:
    appConfig = getJsonConfig()
    fetcher = ScadaDataFetcher(appConfig.api_host, appConfig.api_port)
    overVoltage, underVoltage = voltageBandRange(pnt['voltLvl'])
    voltSamplInd = -1
    recommendation = ''
    isRecommendation = False
    isOverVoltage = False
    isUnderVoltage = False
    if busVolts:
        for sampItr in range(len(busVolts)-2):
            if (busVolts[sampItr] > overVoltage) and (busVolts[sampItr+1] > overVoltage) and (busVolts[sampItr+2] > overVoltage):
                # fetch line reactor data if over voltage exists for atleast 3 mins
                lineReactorDict = fetcher.fetchEdnaData(
                    pnt['lineReactorId'], startTime, endTime)
                voltSamplInd = sampItr+2
                isOverVoltage = True
                break
            if (busVolts[sampItr] < underVoltage) and (busVolts[sampItr+1] < underVoltage) and (busVolts[sampItr+2] < underVoltage):
                # fetch line reactor data if under voltage exists
                lineReactorDict = fetcher.fetchEdnaData(
                    pnt['lineReactorId'], startTime, endTime)
                voltSamplInd = sampItr+2
                isUnderVoltage = True
                break
    # Over Voltage Condition
    if isOverVoltage:
        lineReactorData: dict[str, list[float]] = {}
        for lrPntId in lineReactorDict:
            if len(lineReactorDict[lrPntId]):
                lineReactorData[lrPntId] = lineReactorDict[lrPntId]

        # check if any line reactor was out of service at the time of high voltage, if yes then take that in service
        for lrPntId in lineReactorData:
            if lineReactorData[lrPntId][voltSamplInd] == 0:
                recommendation = "Take Suitable Line Reactor in service"
                isRecommendation = True
                print("Line {0} & recommendation, {1}". format(
                    pnt['SubStation'], recommendation))
                return voltSamplInd, recommendation, isRecommendation

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
            return voltSamplInd, recommendation, isRecommendation

        # if data of no bus reactor or line reactor is available then return no reactors availabe
        if not (len(lineReactorData) and len(busReactorData)):
            recommendation = "Data of no reactor is available"
            isRecommendation = False
            return voltSamplInd, recommendation, isRecommendation

        # check if any bus reactor is out of service at the time of high voltage
        for lrPntId in busReactorData:
            if busReactorData[lrPntId][voltSamplInd] == 0:
                recommendation = "Take Suitable Bus Reactor in service"
                isRecommendation = True
                print("Line {0} & recommendation, {1}". format(
                    pnt['SubStation'], recommendation))
                return voltSamplInd, recommendation, isRecommendation
        # no bus reactor is out of service
        recommendation = "No recommendation: All Bus Reactors are already in service"
        isRecommendation = False
        return voltSamplInd, recommendation, isRecommendation

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
            return voltSamplInd, recommendation, isRecommendation

        # check if any bus reactor was in service at the time of low voltage, if yes then take that out of service
        for lrPntId in busReactorData:
            if busReactorData[lrPntId][voltSamplInd] != 0:
                recommendation = "Take Suitable Bus Reactor out of service"
                isRecommendation = True
                print("Line {0} & recommendation, {1}". format(
                    pnt['SubStation'], recommendation))
                return voltSamplInd, recommendation, isRecommendation

        # filter out line data from line dict
        lineReactorData = {}
        for lrPntId in lineReactorDict:
            if len(lineReactorDict[lrPntId]):
                lineReactorData[lrPntId] = lineReactorDict[lrPntId]

        # if data of no bus reactor or line reactor is available then return no reactors availabe
        if not (len(lineReactorData) and len(busReactorData)):
            recommendation = "Data of no reactor is available"
            isRecommendation = False
            return voltSamplInd, recommendation, isRecommendation

        for lrPntId in lineReactorData:
            if lineReactorData[lrPntId][voltSamplInd] != 0:
                recommendation = "Take Suitable Line Reactor out of service"
                isRecommendation = True
                print("Line {0} & recommendation, {1}". format(
                    pnt['SubStation'], recommendation))
                return voltSamplInd, recommendation, isRecommendation

        # no bus reactor is out of service
        recommendation = "No recommendation: All Bus Reactors are already out of service"
        isRecommendation = False
        return voltSamplInd, recommendation, isRecommendation

    return voltSamplInd, recommendation, isRecommendation
