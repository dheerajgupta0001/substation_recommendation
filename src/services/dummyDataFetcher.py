import datetime as dt
from typing import List
import pandas as pd
from src.typeDefs.fetchPnt import FetchPnt
    

class DummyDataFetcher():
    def fetchPntsData(pnts: List[FetchPnt], startTime: dt.datetime, endTime: dt.datetime) -> dict:
        pntId = pnts.split(",")
        resObj = {}

        global dataDf
        for pnt in pntId:
            resObj[pnt] = []
        for pnt in pntId:
            if pnt in dataDf.columns:
                dataDf = dataDf[(dataDf['time'] >= startTime) & (dataDf['time'] <= endTime)]
                data = dataDf[pnt].to_list()
                resObj[pnt] = data

        return resObj
    
