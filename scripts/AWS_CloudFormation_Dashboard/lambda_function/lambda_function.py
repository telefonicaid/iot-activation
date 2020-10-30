import json
import pymysql
import os

def lambda_handler(event, context):

    rds_host = os.environ.get('DB_HOST')
    name = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASS')
    db_name = os.environ.get('DB_NAME')

    thingName = event["thingName"]
    reported = event["state"]["reported"]["data"]

    try:

        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)

        print("Connected to MySQL Server")

        for sensor in reported:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO sensorData(thingName, sensorKey, value) VALUES(%s, %s, %s)',
                       (thingName, sensor, reported[sensor]))
            conn.commit()

    except:
        print("ERROR")
