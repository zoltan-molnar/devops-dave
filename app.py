import logging

from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS

from utils.config import CONFIG
import mock

app = Flask(__name__)
api = Api(app)
CORS(app)

log_level = logging.getLevelName(CONFIG['log_level'])
logging.basicConfig(level=log_level)


class Main(Resource):

    def get(self):
        logging.info('GET fucntion called')
        return 'get done'

    def post(self):
        logging.info('POST fucntion called')
        return 'post done'

api.add_resource(Main, '/')

if CONFIG['enable_worker_api']:
    api.add_resource(mock.WorkerMock, '/worker/<string:function>')
