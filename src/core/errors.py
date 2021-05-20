#!/usr/bin/env python

class CoreException(Exception):
    """Base Users Exception"""

    message = "An unknown exception occurred."
    code = 500

    def __init__(self, message=None, **kwargs):
        self.code = kwargs.get('code', None) or getattr(self, 'code', None) or 500

        try:
            self.message = str(message) if message else 'Unknown Error'
        except Exception as err:
            self.message = 'Unknown Error'

        super(CoreException, self).__init__(self.message)

    def __str__(self):
        return self.message

    def __unicode__(self):
        return self.message

#------------------------------------------------
#              Server Error(s)
#------------------------------------------------
class ServerError(CoreException):
    message = "%(detail)s"
    code = 500

class UserCreationError(ServerError):
    code = 500

#------------------------------------------------
#              Client Error(s)
#------------------------------------------------
class ClientError(CoreException):
    message = "%(detail)s"
    code = 400

class UserExists(ClientError):
    code = 409

class PasswordMismatch(ClientError):
    code = 400

class NoJWTUserError(ClientError):
    code = 400
    
class BadRequestError(ClientError):
    code = 400
    
class AccessDeniedError(ClientError):
    code = 400