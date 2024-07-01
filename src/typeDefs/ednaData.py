from typing import TypedDict
import datetime as dt

class IEdnaDataInfo(TypedDict):
    dval: float
    timestamp: dt.datetime
    status: str
    units: str