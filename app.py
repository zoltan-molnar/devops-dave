import logging

from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

logging.basicConfig()
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)


class Main(Resource):

    def get(self):
        logging.info('GET fucntion called')

    def post(self):
        logging.info('POST fucntion called')

api.add_resource(Main, '/')
