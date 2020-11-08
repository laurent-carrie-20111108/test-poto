import uuid
import json
from flask_restplus import Namespace, Resource
from flask import request
from project.flask_utils import fix_null_marshalling
from project.core.Connect import CoreConnect
from flask import current_app as app

api = Namespace('core', description='Eldorado Core BlockChain')

@api.route('/health')
class HealthCheck(Resource):
    def get(self):
        """
        Check health of REST API
        ---
        tags:
          - core
        responses:
          200:
            description: Health status of the Python Project
          503:
            description: Error
        """
        return {'health': 'ok', 'project':'core'}, 200

@api.route('/db/health')
class HealthCheckDb(Resource):
    def get(self):
        """
        Check health of the DB Connection
        ---
        tags:
          - core
        responses:
          200:
            description: Health status of the DB Connection. Get total of TXS
          503:
            description: Error + Type of error
        """
        try:
            connect = CoreConnect()
            print('HealthCheck CoreConnect',connect.db)
            cursor = connect.db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS txs (
                  `tid` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                  `rid` varchar(40) NOT NULL,
                  `sid` varchar(40) NOT NULL,
                  `amt` varchar(20) NOT NULL,
                  `status` varchar(40) NOT NULL,
                );
                """
            )
            cursor.execute("SELECT count(*) FROM txs LIMIT 1")
            result = cursor.fetchone()
            return {'health': 'ok', 'project':'db','total_txs':result}, 200
        except Exception as e:
            return {'health': 'error', 'msg':'Error: {}'.format(str(e)),'project':'db'}, 503
