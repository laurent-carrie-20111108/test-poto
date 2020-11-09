import uuid
import json
from flask_restplus import Namespace, Resource
from flask import request
from project.flask_utils import fix_null_marshalling
from project.core.Connect import CoreConnect
from flask import current_app as app
import datetime

api = Namespace('transactions', description='MAP Tx')


@api.route('')
class CreateWallet(Resource):
    def post(self):
        """
        Create a new tx -  a failed tx shall create a transaction with a status "ERROR"
        ---
        tags:
          - transaction
        parameters:
          - in: body
            name: tid
            required: true
            type: string
          - in: body
            name: sid
            required: true
            type: string
          - in: body
            name: rid
            required: true
            type: string
          - in: body
            name: amt
            required: true
            type: integer
          - in: body
            name: date
            required: false
            type: date
        responses:
          200:
            description: Transaction created, Status -  Valided
          400:
            description: Malformed request, Status -  Error
          406:
            description: Amount shall be a number and positif, Status -  Error
          406:
            description: Sender can not be receiver, Status -  Error
          406:
            description: Tid format is not a uuid4 format, Status -  Error
          503:
            description: Unable to create wallet, Status -  Error
        """
        try:

            # because we want to insert a row in the database even in case of error
            # we need to provide default values
            tid = ''
            sid = -1
            rid = -1
            amt = 0

            def insert_transaction_in_db(status):
                """
                insert a row in the database,
                :param status:
                tid, sid, rid and amt provided as closure
                :return:
                """
                connect = CoreConnect()
                cursor = connect.db.cursor()
                date = datetime.datetime.now()
                query = 'INSERT INTO txs (date,tid,rid,sid,amt,status) VALUES (%s, %s, %s, %s, %s, %s)'
                cursor.execute(
                    query, [
                        date,
                        tid,
                        str(rid),
                        str(sid),
                        str(amt),
                        status
                    ]
                )

                connect.db.commit()
                # we want the POST request to return the id of the created row
                cursor.execute('select LAST_INSERT_ID() ;')
                id = cursor.fetchone()
                id = id.get('LAST_INSERT_ID()')
                return id

            def insert_error_row_and_return_error_msg(msg, code):
                """
                inserts an error row with the HTTP return code
                :param msg:
                :param code:
                :return:
                """
                id = insert_transaction_in_db('ERROR')
                return {'msg': msg, 'id': id}, code

            # check the tid input parameter
            tid = request.json.get('tid', None)
            if tid is None:
                # we cannot put NULL in the database because of an SQL constraint
                # we set an arbitrary value that should not be used
                tid = -1
                return insert_error_row_and_return_error_msg('tid is not present', 406)
            try:
                uuid.UUID(str(tid))
            except Exception as e:
                return insert_error_row_and_return_error_msg(f'failed to convert tid to uuid, Error : {e}', 406)

            # check the sid input parameter
            sid = request.json.get('sid', None)
            if sid is None:
                # we cannot put NULL in the database because of an SQL constraint
                # we set an arbitrary value that should not be used
                sid = -1
                return insert_error_row_and_return_error_msg('sid is not present', 406)

            # check the rid input parameter
            rid = request.json.get('rid', None)
            if rid is None:
                # we cannot put NULL in the database because of an SQL constraint
                # we set an arbitrary value that should not be used
                rid = -1
                return insert_error_row_and_return_error_msg('rid is not present', 406)
            if sid == rid:
                return insert_error_row_and_return_error_msg('receiver cannot be sender', 406)

            # check the amt input parameter
            amt = request.json.get('amt', None)
            if amt is None:
                # we cannot put NULL in the database because of an SQL constraint
                # we set an arbitrary value that should not be used
                amt = 0
                return insert_error_row_and_return_error_msg('amt is not present', 406)
            if type(amt) is not int:
                amt = 0
                return insert_error_row_and_return_error_msg('Error: amount is not an integer value', 406)
            if amt < 0:
                return insert_error_row_and_return_error_msg('Error: amount should be positive', 406)

            # at this point, input parameters are correct
            # we can insert in the database
            id = insert_transaction_in_db('OK')
            return {'id': id, 'msg': 'insertion ok'}, 200

        except Exception as e:
            # catch all other exceptions, return 503 as we cannot state the error is caused by wrong input data
            return {'msg': f'Error: {str(e)}', 'project': 'db'}, 503


@api.route('/<int:id>')
class GetWallet(Resource):
    def get(self, id):
        """
        Get an existing tx or error 404 - Not Found -
            this is regardless of the status of the tx : a tx with status ERROR will be returned
            the same way as a tx with status OK
        ---
        tags:
          - transaction
        parameters:
          - in: body
            name: id
            required: true
            type: int
        responses:
          200:
            description: record found and returned
          404:
            description: no record found for that id
          406:
            description: input data is incorrect
          503:
            description: Unable to get wallet, Status -  Error
        """

        try:
            connect = CoreConnect()
            cursor = connect.db.cursor()
            # query
            query = 'SELECT date,tid,rid,sid,amt,status FROM txs where id = %s;'
            cursor.execute(query, [id])
            # get oner row
            row = cursor.fetchone()
            # at this point, the request is successful. It returns either one or zero row
            if row is None:
                return {'id': id, 'msg': 'no row', 'project': 'db'}, 404
            row['date'] = row['date'].strftime('%Y-%m-%d %H:%M:%S')
            return row, 200
        except Exception as e:
            return {'msg': f'Error: {str(e)}', 'project': 'db'}, 503
