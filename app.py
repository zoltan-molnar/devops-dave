import logging

from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS

import mock

app = Flask(__name__)
api = Api(app)
CORS(app)


class Main(Resource):

    def get(self):
        logging.info('GET fucntion called')
        return 'get done'

    def post(self):
        logging.info('POST fucntion called')
        return 'post done'

api.add_resource(Main, '/')

api.add_resource(mock.WorkerMock, '/worker/<string:function>')
