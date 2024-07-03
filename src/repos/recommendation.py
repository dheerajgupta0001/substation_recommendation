import datetime as dt
import psycopg2
from src.typeDefs.fetchPnt import FetchPnt
from src.services.dummyDataFetcher import DummyDataFetcher
from src.config.appConfig import getJsonConfig

dbConfig = getJsonConfig()


def insertToDB(time_stamp: dt.datetime, substation: str, recommendation: str, busVolt: str, isRecommendation: bool):
    dbConn = None
    dbCur = None
    isInsertSuccess = True
    try:
        dbConn = psycopg2.connect(host=dbConfig['db_host'], dbname=dbConfig['db_name'],
                                  user=dbConfig['db_username'], password=dbConfig['db_password'])
        dbCur = dbConn.cursor()
        dbCur.execute(
            'DELETE from "Latest_Recommendation" where substation_name= %s', (substation,))
        dbConn.commit()
        dbCur.execute('INSERT INTO "Latest_Recommendation" (time_stamp, substation_name, recommendation, voltage_str, "isRecommendation") VALUES (%s, %s, %s, %s, %s)',
                      (time_stamp, substation, recommendation, busVolt, isRecommendation))
        dbCur.execute('INSERT INTO "Draft_Recommendation" (time_stamp, substation_name, recommendation, voltage_str, "isRecommendation") VALUES (%s, %s, %s, %s, %s)',
                      (time_stamp, substation, recommendation, busVolt, isRecommendation))
        dbCur.execute('INSERT INTO "Recommendation_History" (time_stamp, substation_name, recommendation, voltage_str, "isRecommendation") VALUES (%s, %s, %s, %s, %s)',
                      (time_stamp, substation, recommendation, busVolt, isRecommendation))
        dbConn.commit()

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
