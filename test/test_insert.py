from flask import url_for
import uuid
from frozendict import frozendict
from project.core.Connect import CoreConnect

# data for a POST request that works
# we freeze it so tests do not have side effects
request = frozendict({
    'tid': uuid.uuid4(),
    'rid': 10,
    'sid': 20,
    'amt': 5
})


def check_row(id, request, status):
    """
    a helper function that checks that the row in the database with id 'id'
    is equal to the dictionary request
    :param id: the id of the tx
    :param request: the data to compare
    :param status: the status to comapre
    :return:
    """
    connect = CoreConnect()
    cursor = connect.db.cursor()
    cursor.execute(f'SELECT tid,rid,sid,amt,status from txs where id = {id};')
    row = cursor.fetchone()
    assert row['amt'] == request['amt']
    assert row['rid'] == request['rid']
    assert row['sid'] == request['sid']
    assert row['tid'] == str(request['tid'])
    assert row['status'] == status


def check_row_error(id):
    """
    checks that the row with id 'id' has the status set as ERROR
    :param id:
    :return:
    """
    connect = CoreConnect()
    cursor = connect.db.cursor()
    cursor.execute(f'SELECT status from txs where id = {id};')
    row = cursor.fetchone()
    assert row['status'] == 'ERROR'


class TestInsert:

    def setup_method(self, test_method):
        """
            each test should start from a deterministic state
            we just clean the txs the table

            the other way would be to prevent committing,
        """
        connect = CoreConnect()
        cursor = connect.db.cursor()
        cursor.execute('DELETE FROM txs ;')
        connect.db.commit()

    def test_insert_ok(self, client):
        """
        check that insertion of correct data returns 200
        and that data is correctly inserted
        :param client:
        :return:
        """
        res = client.post(url_for('transactions_create_wallet'), json=dict(request))
        assert res.status_code == 200
        assert res.json['msg'] == 'insertion ok'
        id = res.json['id']
        check_row(id, dict(request), 'OK')

    def test_insert_missing_input(self, client):
        """
        check that a missing parameter request returns 406
        check that the data is correctly inserted with ERROR status
        :param client:
        :return:
        """
        for arg_name in request.keys():
            d = dict(request.copy())
            d.pop(arg_name)
            res = client.post(url_for('transactions_create_wallet'), json=d)
            assert res.status_code == 406
            assert res.json['msg'] == f'{arg_name} is not present'
            id = res.json['id']
            check_row_error(id)

    def test_insert_bad_uuid(self, client):
        """
        check the behaviour if tid is not a correct uuid
        check that the data is correctly inserted with ERROR status
        :param client:
        :return:
        """
        d = dict(request.copy())
        d['tid'] = '8976d'
        res = client.post(url_for('transactions_create_wallet'), json=d)
        assert res.status_code == 406
        assert res.json['msg'] == 'failed to convert tid to uuid, Error : badly formed hexadecimal UUID string'
        id = res.json['id']
        check_row_error(id)

    def test_insert_negative_amount(self, client):
        """
        check the behaviour in case of negative amount
        check that the data is correctly inserted with ERROR status
        :param client:
        :return:
        """
        d = dict(request.copy())
        d['amt'] = -3
        res = client.post(url_for('transactions_create_wallet'), json=d)
        assert res.status_code == 406
        assert res.json['msg'] == 'Error: amount should be positive'
        id = res.json['id']
        check_row_error(id)

    def test_insert_non_int_amount(self, client):
        """
        check the behaviour in case the amount is not an integer value
        check that the data is correctly inserted with ERROR status
        :param client:
        :return:
        """
        d = dict(request)
        d['amt'] = 'I am not an int'
        res = client.post(url_for('transactions_create_wallet'), json=d)
        assert res.status_code == 406
        assert res.json['msg'] == 'Error: amount is not an integer value'
        id = res.json['id']
        check_row_error(id)

    def test_insert_receiver_cannot_be_sender(self, client):
        """
        check the behaviour in case the receiver is equal to the sender
        check that the data is correctly inserted with ERROR status
        :param client:
        :return:
        """
        d = dict(request)
        d['rid'] = d['sid']
        res = client.post(url_for('transactions_create_wallet'), json=d)
        assert res.status_code == 406
        assert res.json['msg'] == 'receiver cannot be sender'
        id = res.json['id']
        check_row_error(id)
