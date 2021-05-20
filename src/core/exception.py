import functools
import json
import logging
import re
import uuid


import flask
import werkzeug

from src.core.errors import CoreException
from flask_jwt_extended.exceptions import NoAuthorizationError, RevokedTokenError

log = logging.getLogger(__name__)


SERVER_ERRORS = {
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
}
OBFUSCATED_MSG = (
    'Your request could not be handled because'
    ' of a problem in the server. '
    'Error Correlation id is: %s'
)


def wrap_controller_exception(func, func_server_error, func_client_error):
    """This decorator wraps controllers methods to handle exceptions"""
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as excp:
            if isinstance(excp, CoreException):
                http_error_code = getattr(excp, 'code', 500)
            elif isinstance(excp, werkzeug.exceptions.HTTPException):
                http_error_code = getattr(excp, 'code', 500)
            elif isinstance(excp, (NoAuthorizationError, RevokedTokenError)):
                http_error_code = 401
            else:
                http_error_code = 500

            if http_error_code >= 500:
                # log the error message with its associated
                # correlation id
                log_correlation_id = str(uuid.uuid4())
                log.exception("%(correlation_id)s:%(excp)s",
                              {'correlation_id': log_correlation_id,
                               'excp': str(excp)})
                # raise a server error with an obfuscated message
                return func_server_error(log_correlation_id, http_error_code)
            else:
                # raise a client error the original message
                log.debug(excp)
                return func_client_error(excp, http_error_code)
    return wrapped


def convert_excp_to_err_code(excp_name):
    """Convert Exception class name (CamelCase) to error-code (Snake-case)"""
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+',
                       excp_name)
    return '-'.join([str.lower(word) for word in words])


def wrap_api_exception(func):
    """This decorator wraps apis to handle exceptions."""

    def _details(excp):
        try:
            if isinstance(excp, CoreException):
                return str(excp)
            elif isinstance(excp, werkzeug.exceptions.HTTPException):
                return '%s' % (excp.data if excp.data else excp.description)
            else:
                return str(excp.args[0])
        except Exception as err:
            _ = err
            return "ERROR: Can not fetch error details from exception"

    def _func_server_error(log_correlation_id, status_code):
        response = {
            'faultcode': 'Server',
            'status': status_code,
            'result': SERVER_ERRORS[status_code],
            'message': OBFUSCATED_MSG % log_correlation_id,
        }
        return flask.current_app.response_class(
            json.dumps(response), status=status_code,
            mimetype='application/json')

    def _func_client_error(excp, status_code):
        response = {
            'faultcode': 'Client',
            'faultstring': convert_excp_to_err_code(excp.__class__.__name__),
            'status': status_code,
            'result': str(excp),
            'message': _details(excp),
        }
        return flask.current_app.response_class(
            json.dumps(response), status=status_code,
            mimetype='application/json')
    return wrap_controller_exception(func, _func_server_error,
                                     _func_client_error)
