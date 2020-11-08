from flask import url_for

from pytest_flask.plugin import JSONResponse


class TestHealth:

    def test_health(self, client):
        res: JSONResponse = client.get(url_for('core_health_check'))
        assert res.status_code == 200
        assert res.json == {'health': 'ok', 'project': 'core'}

    def test_health_db(self, client):
        res = client.get(url_for('core_health_check_db'))
        assert res.json['health'] == 'ok'
        assert res.status_code == 200
        assert res.json['project'] == 'db'
