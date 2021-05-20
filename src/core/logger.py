import logging
import logging.handlers
import os
import time


def create_log_dir(log_dir):
    """
    Create Log directory
    """
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    except Exception as e:
        raise RuntimeError(
            "Failed to create log directory %s due to %s" % (log_dir, e))


def setup_logging(log_dir, log_level, file_size, backup_count, formatter):
    """
    Sets up Logging handlers and other environment.
    """
    log_file = 'controller.log'
    log_file_error = 'controller-error.log'
    create_log_dir(log_dir)
    log_file_name = os.path.join(log_dir, log_file)
    log_file_name_error = os.path.join(log_dir, log_file_error)
    log_formatter = logging.Formatter(formatter)
    log_formatter.converter = time.gmtime
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return
    file_handler = logging.handlers.RotatingFileHandler(
        log_file_name, maxBytes=file_size, backupCount=backup_count)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(getattr(logging, log_level.upper()))
    root_logger.addHandler(file_handler)

    file_handler_error = logging.handlers.RotatingFileHandler(
        log_file_name_error, maxBytes=file_size, backupCount=backup_count)
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    root_logger.addHandler(file_handler_error)
    root_logger.setLevel(getattr(logging, log_level.upper()))
    return root_logger
