from pymysql.constants import CLIENT
import pymysql
# import boto3
from flask import current_app as app


class CoreConnect:
    """Init Start conection pools"""
    # DEFAULT KEYSPACES
    keyspace = 'transactions'

    def __init__(self, mode=None):
        self.init_db()

    # Initilization Mysql Database
    def init_db(self):
        try:
            print(app.config['MYSQL_DB'])
            self.db = pymysql.connect(
                host=app.config['MYSQL_DB']['MYSQL_DATABASE_HOST'],
                user=app.config['MYSQL_DB']['MYSQL_DATABASE_USER'],
                password=app.config['MYSQL_DB']['MYSQL_DATABASE_PASSWORD'],
                db=app.config['MYSQL_DB']['MYSQL_DATABASE_DB'],
                port=3306,
                cursorclass=pymysql.cursors.DictCursor,
                client_flag=CLIENT.MULTI_STATEMENTS,

            )

            return self.db
        except pymysql.Error as e:
            print('ERROR', e)
            return None
