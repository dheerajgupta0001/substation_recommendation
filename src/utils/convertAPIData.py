
def convertData(resObj: dict)->dict[str,list[float]]:
    # the result dict will be like {"meas1": [val1,val2,...], "meas2": [val1,val2,...]}
    finalData = {}
    for temp in resObj:
        finalData[temp] =[]
        for val in resObj[temp]:
            finalData[temp].append(val['dval'])
    return finalData
        