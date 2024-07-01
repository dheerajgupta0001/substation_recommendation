

def checkReasonabilityLimit(dataDict: dict):
    reasonabilityLimit = 100
    for res in dataDict:
        temp = dataDict[res]
        if not any(x <= reasonabilityLimit for x in temp):
            busVolt = temp
            return busVolt

    
