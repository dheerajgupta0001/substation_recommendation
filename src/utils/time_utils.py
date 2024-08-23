import datetime as dt


def convertTimeToReqStr(timeObj: dt.datetime) -> str:
    dateStr = timeObj.strftime('%d/%m/%Y')
    timeStr = "{0}/{1}:{2}:00".format(dateStr, makeTwoDigits(
        timeObj.hour), makeTwoDigits(timeObj.minute))
    return timeStr


def makeTwoDigits(num: int) -> str:
    if (num < 10):
        return "0"+str(num)
    return str(num)
