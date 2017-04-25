from flask import request
from flask_restful import Resource

import worker


class WorkerMock(Resource):
    def get(self, **kwargs):
        function_mock = getattr(worker, kwargs.get('function'))
        return function_mock(None, None)

    def post(self, **kwargs):
        function_mock = getattr(worker, kwargs.get('function'))
        return function_mock(request.get_json(), None)
