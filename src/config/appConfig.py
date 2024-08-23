import pandas as pd
import json
from src.config.jsonConfig import JsonConfig


# def getConfig():
#     configDf = pd.read_excel(
#         'config.xlsx', sheet_name='config', header=None, index_col=0)
#     configDict = configDf[1].to_dict()
#     return configDict


def getPnts() -> list[dict[str, any]]:
    pntsDf = pd.read_excel('config.xlsx', sheet_name='pnts')
    pntsDf = pntsDf.fillna("")
    pntsDict = pntsDf.to_dict('records')
    return pntsDict


def loadJsonConfig(fName="config.json") -> JsonConfig:
    global jsonConfig
    with open(fName) as f:
        data = json.load(f)
        jsonConfig = JsonConfig(**data)
        return jsonConfig


def getJsonConfig() -> JsonConfig:
    global jsonConfig
    return jsonConfig
