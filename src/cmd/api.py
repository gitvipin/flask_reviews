import logging
import signal
import sys

from flask import Flask


from src.api.v1.controller import ControllerApi
from src.api.v1.apps import jwt, reviews_db
from src.core.logger import setup_logging
from src.core.config import LoggingConf, controller_config


class ControllerApiService(object):

    def __init__(self, logger=None):
        self.log = logger if logger else logging.getLogger(__name__)

    def init_app(self, config):
        self.log.info("-----Initializing Controller APP------")
        app = Flask("controller")

        self.app = app
        self.app.config.from_object(config)

        jwt.init_app(app)   # Initialize JWT app

        @app.before_first_request
        def create_tables():
            reviews_db.create_all()

        self.log.info("-----Controller APP Initialized------")

    def init_api(self):
        self.log.info("-----Initializing API------")
        self.api_app = ControllerApi(self.app)
        self.log.info("-----API Initialized------")

    def handle_hup(self):
        self.log.info("Hang up",)

    def handle_term(self, signum, frame):
        "SIGTERM handling"
        self.handle_stop_signals(signum, frame)

    def handle_int(self, signum, frame):
        "SIGINT handling"
        self.handle_stop_signals(signum, frame)

    def handle_stop_signals(self, signum, frame):
        self.log.warning(
            "Received kill signal number %s, "
            "shutting down scheduler" % signum)
        self.log.info("==========Controller App Stopped Successfully=========")
        sys.exit(0)

    def run(self, config):
        self.log.info("==========Starting Controller App=========")
        signal.signal(signal.SIGINT, self.handle_int)
        signal.signal(signal.SIGTERM, self.handle_term)
        signal.signal(signal.SIGHUP, self.handle_hup)
        self.init_app(config)
        self.init_api()
        self.app.run(host=config.CONTROLLER_HOST, port=config.CONTROLLER_PORT,
                     debug=config.DEBUG)


def main():
    logger = None
    try:
        logging.getLogger('werkzeug').setLevel('ERROR')
        logger = setup_logging(
            LoggingConf.LOG_DIR, LoggingConf.LOG_LEVEL,
            LoggingConf.FILE_SIZE, LoggingConf.BACKUP_COUNT,
            LoggingConf.FORMATTER)

        ControllerApiService(logger=logger).run(controller_config)
    except Exception as ex:
        if logger:
            logger.exception("Failed to start Controller App")
        else:
            print("Failed to start Controller app due to : %s" % ex)
        sys.exit(1)


if __name__ == "__main__":
    main()
