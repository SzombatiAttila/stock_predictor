# pylint:disable=missing-module-docstring, no-name-in-module, import-error, missing-function-docstring
import pymysql
from google.cloud import secretmanager
from peewee import MySQLDatabase


def get_secrets():
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/crawling-315317/secrets/DB_PASSWORD/versions/1"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload


def get_mysql_db(password):
    mysql_db = MySQLDatabase(
        user='root',
        password=password,
        unix_socket="/cloudsql/crawling-315317:europe-west1:mysql-03",
        database='twitter',
    )
    return mysql_db


def init_database(password: str, database: str = 'twitter'):
    conn = pymysql.connect(
        unix_socket="/cloudsql/crawling-315317:europe-west1:mysql-03",
        user='root',
        password=password,
    )

    sql = f'CREATE DATABASE IF NOT EXISTS {database}'
    conn.cursor().execute(sql)
    conn.close()
