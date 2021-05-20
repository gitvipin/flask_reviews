#!/bin/env/python
import datetime
import functools
import logging

import src.core.constants as constants

from src.core.errors import NoJWTUserError, AccessDeniedError
from src.core.exception import wrap_api_exception

from flask_jwt_extended import jwt_required, get_jwt_claims, \
    create_access_token, create_refresh_token

log = logging.getLogger(__name__)


def get_utc_time():
    return datetime.datetime.utcnow().strftime(constants.TIME_FORMAT)


def str_to_utc(date):
    return datetime.datetime.strptime(date, constants.TIME_FORMAT)


class JWTUser(object):

    def __init__(self, user_id, is_guest):
        self._user_id = user_id
        self._is_guest = is_guest

    @property
    def is_guest(self):
        return self._is_guest == constants.YES

    @property
    def uid(self):
        return self._user_id


@jwt_required
def get_jwt_user():
    claims = get_jwt_claims()
    user_id = claims.get('uid', None)
    is_guest = claims.get('guest', None)

    jwt_user = JWTUser(user_id, is_guest)

    if not user_id:
        raise NoJWTUserError("No user info in JWT")

    return jwt_user


def get_jwt_tokens(_token_data):
    access_token = create_access_token(identity=_token_data, expires_delta=None)
    refresh_token = create_refresh_token(identity=_token_data)

    return access_token, refresh_token


def jwt_registered(func):
    @functools.wraps(func)
    @wrap_api_exception
    @jwt_required
    def _helper(*args, **kwargs):
        user = get_jwt_user()
        if user.is_guest:
            raise AccessDeniedError("Operation not allowed for Guest user")
        return func(*args, **kwargs)
    return _helper