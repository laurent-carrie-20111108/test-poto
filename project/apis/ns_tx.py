import uuid
import json
from flask_restplus import Namespace, Resource
from flask import request
from project.flask_utils import fix_null_marshalling
from project.core.Connect import CoreConnect
from flask import current_app as app

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
        return True;
