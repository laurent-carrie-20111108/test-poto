from flask import url_for
import uuid
from frozendict import frozendict
from project.core.Connect import CoreConnect


request = frozendict({
    'tid': uuid.uuid4(),
    'rid': 10,
    'sid': 20,
    'amt': 5
})


def check_row(id, request, status):
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
    connect = CoreConnect()
    cursor = connect.db.cursor()
    cursor.execute(f'SELECT status from txs where id = {id};')
    row = cursor.fetchone()
    assert row['status'] == 'ERROR'


class TestInsert:

    def test_insert_ok(self, client):
        res = client.post(url_for('transactions_create_wallet'), json=dict(request))
        assert res.status_code == 200
        assert res.json['msg'] == 'insertion ok'
        id = res.json['id']
        check_row(id, dict(request), 'OK')

    def test_insert_missing_input(self, client):
        for arg_name in request.keys():
            d = dict(request.copy())
            d.pop(arg_name)
            res = client.post(url_for('transactions_create_wallet'), json=d)
            assert res.status_code == 406
            assert res.json['msg'] == f'{arg_name} is not present'
            id = res.json['id']
            check_row_error(id)

    def test_insert_bad_uuid(self, client):
        d = dict(request.copy())
        d['tid'] = '8976d'
        res = client.post(url_for('transactions_create_wallet'), json=d)
        assert res.status_code == 406
        assert res.json['msg'] == 'failed to convert tid to uuid, Error : badly formed hexadecimal UUID string'
        id = res.json['id']
        check_row_error(id)

    def test_insert_negative_amount(self, client):
        d = dict(request.copy())
        d['amt'] = -3
        res = client.post(url_for('transactions_create_wallet'), json=d)
        assert res.status_code == 406
        assert res.json['msg'] == 'Error: amount should be positive'
        id = res.json['id']
        check_row_error(id)

    def test_insert_non_int_amount(self, client):
        d = dict(request)
        d['amt'] = 'I am not an int'
        res = client.post(url_for('transactions_create_wallet'), json=d)
        assert res.status_code == 406
        assert res.json['msg'] == 'Error: amount is not an integer value'
        id = res.json['id']
        check_row_error(id)

    def test_insert_receiver_cannot_be_sender(self, client):
        d = dict(request)
        d['rid'] = d['sid']
        res = client.post(url_for('transactions_create_wallet'), json=d)
        assert res.status_code == 406
        assert res.json['msg'] == 'receiver cannot be sender'
        id = res.json['id']
        check_row_error(id)
