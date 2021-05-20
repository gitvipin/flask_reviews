'''
This module has implementation of top level routes for all the
fron-end facing APIs.

All the routes have been kept here at one place, so as it is easy to
maintain these and also easier to put validation, whitelisting etc
at this one common place.
'''
import logging


from flask import jsonify, Response, request
from flask_jwt_extended import jwt_required, get_jwt_claims

import src.core.constants as constants

from src.core.config import controller_config
from src.core.exception import wrap_api_exception
# from src.core.exception import *
from src.core.errors import CoreException
from src.core.utils import get_jwt_user, jwt_registered

from src.core.errors import BadRequestError

log = logging.getLogger(__name__)

# Tokens APIs
class RouteHandler(object):

    def __init__(self):
        log.info("Init RouteHandler with impl : %s", controller_config.ENDPOINT)

    def _form_response(self, response=None, statusCode=None):
        httpStatusCode = statusCode or 200
        if httpStatusCode >= 400:
            raise CoreException(message=response['developer_message'],code=httpStatusCode)

        if response is None:
            return {}, httpStatusCode

        if 'user_id' in response:
            response.pop('user_id')

        if isinstance(response,list):
            for obj in response:
                obj.pop('user_id',None)
        return jsonify({
                        'result':response,
                        'status':200,
                        'success':True
                        }), httpStatusCode

    @wrap_api_exception
    def hello(self):
        res = {
            'message':"Welcome to Demo API !!",
            'result': {},
            'status': 200
        }
        return jsonify(res), 200

    @jwt_registered
    def create_business(self):
        user_id = get_jwt_user().uid
        data = 'hello'
        if 'user_id' in data:
            raise BadRequestError("Invalid Request.user_id is not allowed in request")
        data['user_id'] = user_id
        result,statusCode = self._businesses.post(data)
        return self._form_response(result,statusCode)

    @jwt_required
    @wrap_api_exception
    def get_business(self, bid):
        user_id = get_jwt_user().uid
        result,statusCode = self._businesses.get(user_id, bid)
        return self._form_response(result,statusCode)

   