from project.core.Connect import CoreConnect
from project.core.CodeMapper import CodeMapper
from project.core.order import Order


class BalanceInsufficient(Exception):
    status_code = 400

    def __init__(self, connect, message, tx: Order, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.vitess = connect.vitess
        self.code_mapper = CodeMapper()
        self.create_transaction(tx)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

    def create_transaction(self, tx: Order):
        self.vitess.rollback()
        query = 'INSERT INTO eldoradodev.trx (tid, sid, rid, amt, currency, sign, reason, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

        cursor = self.vitess.cursor()
        cursor.execute(
            query, [
                str(tx.tid),
                str(tx.sender_uid),
                str(tx.receiver_uid),
                tx.amount,
                tx.currency,
                'sign',
                self.code_mapper.get_reason('insufficient-balance'),
                self.code_mapper.get_type('error')
            ]
        )

        self.vitess.commit()
