from flask import url_for
import uuid
from project.core.Connect import CoreConnect

import datetime


class TestGet:

    # each test should start from a deterministic state
    # we just clean the txs the table
    #
    # the other way would be to prevent committing,
    def setup_method(self, test_method):
        connect = CoreConnect()
        cursor = connect.db.cursor()
        cursor.execute('DELETE FROM txs ;')
        connect.db.commit()

    def test_get(self, client):
        """
        insert data in the database, retrieve it with a GET request,
        and check they are the same
        :param client:
        :return:
        """
        connect = CoreConnect()
        cursor = connect.db.cursor()
        # create data to insert in the db
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tid = uuid.uuid4()
        sid = 3
        rid = 9
        amt = 78
        status = 'OK'
        cursor.execute(
            f"INSERT INTO txs (date,tid,rid,sid,amt,status) VALUES ('{date}','{tid}','{rid}','{sid}',{amt},'{status}') ;")
        connect.db.commit()
        # retrieve the id of the newly inserted row
        cursor.execute('select LAST_INSERT_ID() ;')
        id = cursor.fetchone()
        id = id.get('LAST_INSERT_ID()')

        # use the API to retrieve the same data
        res = client.get(url_for('transactions_get_wallet', id=id))
        assert res.status_code == 200
        assert res.json == {'amt': amt, 'sid': sid, 'rid': rid, 'status': status, 'tid': str(
            tid), 'date': date}

    def test_404(self, client):
        """
        test the behaviour of the GET method on a non existing id
        :param client:
        :return:
        """

        id = 42
        # the setup method removes all row from the database
        # so we know the row with id 'id' does not exist

        res = client.get(url_for('transactions_get_wallet', id=id))
        assert res.status_code == 404
