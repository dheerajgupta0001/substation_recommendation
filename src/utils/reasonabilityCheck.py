

def getReasonableVoltVals(dataDict: dict[str, list[float]])->list[float]:
    # returns the first resonable bus voltage values from multiple bus voltages 
    reasonabilityLimit = 100
    for res in dataDict:
        temp = dataDict[res]
        if not any(x <= reasonabilityLimit for x in temp):
            busVolt = temp
            return busVolt
    return []