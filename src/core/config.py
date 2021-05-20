import datetime
import os


basedir = os.getenv(
    'CONTROLLER_DIR', os.path.abspath(os.path.dirname(__file__)))


class LoggingConf:
    LOG_LEVEL = os.getenv("LOG_LEVEL", 'INFO')
    LOG_DIR = os.getenv("LOG_DIR", "/var/log/api_example")
    FILE_SIZE = os.getenv("FILE_SIZE", 3 * (10 ** 6))  # 30 MBs
    BACKUP_COUNT = os.getenv("BACKUP_COUNT", 20)
    FORMATTER = os.getenv(
        "LOG_FORMATTER",
        '%(asctime)s::%(levelname)s::%(name)s[%(lineno)04s]::%(message)s'
    )


class Config:

    PROJECT_NAME = os.getenv('PROJECT_NAME', 'ApiExample')
    CONTROLLER_HOST = '0.0.0.0'
    CONTROLLER_PORT = os.getenv('CONTROLLER_PORT', 5000)
    DATABASE = os.getenv('DATABASE_TYPE', 'sql')
    DEBUG = False
    ENDPOINT = 'ext'    # use sqlite database

    # JWT Tokens
    SECRET_KEY = os.getenv('SECRET_KEY', 'Salesforce')
    SESSION_TYPE = os.getenv('SESSION_TYPE')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'Salesforce')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    _token_expire = os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 30*60)
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=int(_token_expire))

    # Let all the errors be reported at once from flask_restful.reqparse
    # HELP: https://flask-restful.readthedocs.io/en/latest/reqparse.html#error-handling
    BUNDLE_ERRORS = True

    @staticmethod
    def init_app(app):
        pass


class DevEnvConfig(Config):
    DEBUG = True


class TestEnvConfig(Config):
    TESTING = True


class ProdEnvConfig(Config):
    pass


app_config = {
    'dev': DevEnvConfig,
    'test': TestEnvConfig,
    'prod': ProdEnvConfig,
    'default': ProdEnvConfig
}

controller_config = app_config[os.getenv('CONTROLLER_ENV', 'default')]
