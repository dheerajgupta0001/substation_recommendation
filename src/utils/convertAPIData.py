
def convertData(resObj: dict):
    finalData = {}
    for temp in resObj:
        finalData[temp] =[]
        # listOfData = []
        for val in resObj[temp]:
            finalData[temp].append(val['dval'])
            
        # finalData[temp] = listOfData

    return finalData
        