from flask import url_for
import uuid
from frozendict import frozendict
from project.core.Connect import CoreConnect

import datetime
import time


class TestGet:

    def test_get(self, client):
        connect = CoreConnect()
        cursor = connect.db.cursor()
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tid = uuid.uuid4()
        sid = 3
        rid = 9
        amt = 78
        status = 'OK'
        cursor.execute(
            f"INSERT INTO txs (date,tid,rid,sid,amt,status) VALUES ('{date}','{tid}','{rid}','{sid}',{amt},'{status}') ;")
        connect.db.commit()
        cursor.execute('select LAST_INSERT_ID() ;')
        id = cursor.fetchone()
        id = id.get('LAST_INSERT_ID()')

        res = client.get(url_for('transactions_get_wallet', id=id))
        assert res.status_code == 200
        assert res.json == {'amt': amt, 'sid': sid, 'rid': rid, 'status': status, 'tid': str(
            tid), 'date': date}

    def test_404(self, client):
        connect = CoreConnect()
        cursor = connect.db.cursor()
        id = 42
        cursor.execute(
            f'DELETE FROM txs where id = {id} ;')
        connect.db.commit()

        res = client.get(url_for('transactions_get_wallet', id=id))
        assert res.status_code == 404
