import datetime as dt
import os
import pandas as pd
import requests
import json
from src.utils.time_utils import convertTimeToReqStr
from src.utils.convertAPIData import convertData

class ScadaDataFetcher():
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def fetchEdnaData(self, pntId, from_time, to_time):
        from_time_str = convertTimeToReqStr(from_time)
        to_time_str = convertTimeToReqStr(to_time)
        meas_list = pntId.split(",")
        # print(req_date_str)
        # initializing the result object
        resObj = {}
        for meas_Id in meas_list:
            resObj[meas_Id] = []

        for meas_Id in meas_list:
            params = dict(
                pnt=meas_Id,
                strtime=from_time_str,
                endtime=to_time_str,
                secs=60,
                type="snap"
            )
            r = requests.get(
                url="http://{0}:{1}/api/values/history".format(self.host, self.port), params=params)
            data = json.loads(r.text)
            resObj[meas_Id] = data

        resObj = convertData(resObj)
        return resObj