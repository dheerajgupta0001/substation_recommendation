import datetime as dt
import psycopg2
from src.typeDefs.fetchPnt import FetchPnt
from src.services.dummyDataFetcher import DummyDataFetcher
from src.config.appConfig import getJsonConfig

dbConfig = getJsonConfig()


def insertRecomToHistory(time_stamp: dt.datetime, substation: str, recommendation: str, busVoltsStr: str, isRecommendation: bool, openRecomId: int, iterationStartTime: dt.datetime):
    dbConn = None
    dbCur = None
    isInsertSuccess = False
    try:
        dbConn = psycopg2.connect(host=dbConfig['db_host'], dbname=dbConfig['db_name'],
                                  user=dbConfig['db_username'], password=dbConfig['db_password'])
        dbCur = dbConn.cursor()
        # dbCur.execute(
        #     'DELETE from "Latest_Recommendation" where substation_name= %s', (substation,))
        # dbConn.commit()
        # dbCur.execute('INSERT INTO "Latest_Recommendation" (time_stamp, substation_name, recommendation, voltage_str, "isRecommendation") VALUES (%s, %s, %s, %s, %s)',
        #               (time_stamp, substation, recommendation, busVoltsStr, isRecommendation))
        # dbCur.execute('INSERT INTO "Draft_Recommendation" (time_stamp, substation_name, recommendation, voltage_str, "isRecommendation") VALUES (%s, %s, %s, %s, %s)',
        #               (time_stamp, substation, recommendation, busVoltsStr, isRecommendation))
        if openRecomId == -1:
            # if an open recommendation does not exist, then insert the recommendation
            dbCur.execute('INSERT INTO "Recommendation_History" (time_stamp, substation_name, recommendation, voltage_str, "isRecommendation", latest_alert_time) VALUES (%s, %s, %s, %s, %s, %s)',
                          (time_stamp, substation, recommendation, busVoltsStr, isRecommendation, iterationStartTime))
        else:
            # if an open recommendation exists, then update the latest_alert_time to the recommendation timestamp
            dbCur.execute(
                'UPDATE "Recommendation_History" set latest_alert_time=%s where id=%s', (iterationStartTime, openRecomId))
        dbConn.commit()

        isInsertSuccess = True

    except Exception as err:
        isInsertSuccess = False
        print('Error while inserting unit name for {} from master table'.format())
        print(err)

    finally:
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    return isInsertSuccess


def deleteFromDraftDB(startTime: dt.datetime):
    dbConn = psycopg2.connect(host=dbConfig['db_host'], dbname=dbConfig['db_name'],
                              user=dbConfig['db_username'], password=dbConfig['db_password'])
    dbCur = dbConn.cursor()
    dbCur.execute('DELETE FROM "Draft_Recommendation"')
    dbCur.execute(
        'DELETE from "Latest_Recommendation" where time_stamp < %s', (startTime, ))
    dbConn.commit()


def getOpenRecomId(substation: str, recommendation: str) -> int:
    dbConn = None
    dbCur = None
    try:
        dbConn = psycopg2.connect(host=dbConfig['db_host'], dbname=dbConfig['db_name'],
                                  user=dbConfig['db_username'], password=dbConfig['db_password'])
        dbCur = dbConn.cursor()
        dbCur.execute('select "Id" from "Recommendation_History" where substation_name = %s and recommendation = %s and revival_time is null',
                      (substation, recommendation))
        records = dbCur.fetchall()
        if len(records) == 0:
            return -1
        matchingRowId = records[0][0]
        return matchingRowId

    except Exception as err:
        print('Error while checking existing entry for substation {} from Recommendation_History '.format(
            substation))
        print(err)

    finally:
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    return -1


def updateHREndTimeDB(startTime: dt.datetime, subStationList: list):
    try:
        dbConn = psycopg2.connect(host=dbConfig['db_host'], dbname=dbConfig['db_name'],
                                  user=dbConfig['db_username'], password=dbConfig['db_password'])
        dbCur = dbConn.cursor()
        # update revival time of in band substation
        latestRecords = tuple(subStationList)
        dbCur.execute(
            'UPDATE "Recommendation_History" SET revival_time = %s where time_stamp < %s and substation_name not in %s', (startTime, startTime, latestRecords,))
        dbConn.commit()

    except Exception as err:
        isInsertSuccess = False
        print(err)


def updateLatestRecoms() -> bool:
    isSuccess = False
    try:
        dbConn = psycopg2.connect(host=dbConfig['db_host'], dbname=dbConfig['db_name'],
                                  user=dbConfig['db_username'], password=dbConfig['db_password'])
        dbCur = dbConn.cursor()
        # update revival time of in band substation
        dbCur.execute('DELETE FROM "Latest_Recommendation"')
        dbCur.execute('insert into "Latest_Recommendation" (time_stamp, substation_name, recommendation, voltage_str, "isRecommendation") (select time_stamp, substation_name, recommendation, voltage_str, "isRecommendation" from "Recommendation_History" where revival_time is null)')
        dbConn.commit()
        isSuccess = True
    except Exception as err:
        isSuccess = False
        print(err)

    finally:
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isSuccess


def markRecomsAsClosed(iterationTime: dt.datetime) -> bool:
    isSuccess = False
    # Find all the open recommendations where the latest_alert_time < iterationTime and set the revival time as the latest_alert_time
    try:
        dbConn = psycopg2.connect(host=dbConfig['db_host'], dbname=dbConfig['db_name'],
                                  user=dbConfig['db_username'], password=dbConfig['db_password'])
        dbCur = dbConn.cursor()
        dbCur.execute(
            'update "Recommendation_History" set revival_time=latest_alert_time where (revival_time is null) and (latest_alert_time<%s)', (iterationTime,))
        dbConn.commit()
        isSuccess = True
    except Exception as err:
        isSuccess = False
        print(err)

    finally:
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isSuccess
