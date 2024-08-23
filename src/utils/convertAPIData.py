
def convertData(fetchedObj: dict) -> dict[str, list[float]]:
    # input dictionary will be like 
    # {"meas1": [
    #   {"dval":<float>,"timestamp":<str>,"status":<str>},
    #   {"dval":<float>,"timestamp":<str>,"status":<str>},
    # ...
    # ], 
    # "meas2": [...]
    # }
    # 
    # the result dict will be like {"meas1": [val1,val2,...], "meas2": [val1,val2,...]}
    finalData = {}
    for measId in fetchedObj:
        finalData[measId] = []
        for dataSample in fetchedObj[measId]:
            finalData[measId].append(dataSample['dval'])
    return finalData
