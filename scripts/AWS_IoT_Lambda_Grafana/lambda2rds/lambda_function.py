import json
import pymysql
import rds_config


def lambda_handler(event, context):
    rds_host = rds_config.db_endpoint
    name = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    port = 3306

    reported = event["state"]["reported"]

    # for sensor in reported:
    #     print(sensor)
    #     print(reported[sensor])

    try:

        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)

        print("Connected to MySQL Server")

        cursor = conn.cursor()
        cursor.execute('INSERT INTO data(temp, hum) VALUES(%s, %s)',
                       (reported["temp"], reported["hum"]))
        conn.commit()

    except:
        print("ERROR")