import pandas as pd
import json

def getConfig():
    configDf = pd.read_excel(
        'config.xlsx', sheet_name='config', header=None, index_col=0)
    configDict = configDf[1].to_dict()
    return configDict

def getPnts():
    pntsDf = pd.read_excel('config.xlsx', sheet_name='pnts')
    pntsDf = pntsDf.fillna("")
    pntsDict = pntsDf.to_dict('records')
    return pntsDict

def getJsonConfig(fName="config.json") -> dict:
    global jsonConfig
    with open(fName) as f:
        data = json.load(f)
        jsonConfig = data
        return jsonConfig
