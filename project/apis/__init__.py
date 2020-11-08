from flask_restplus import Api

from .ns_core import api as ns_core
from .ns_tx import api as ns_tx

api = Api(
    title='Test Python MAP',
    version='1.0',
    description='Test Python Mon Ami Poto',
)

api.add_namespace(ns_core, path='/core')
api.add_namespace(ns_tx, path='/core/transactions')
