import logging
import os
from logging.handlers import RotatingFileHandler

from src.constants.config import LOG_DIR
from src.constants.logger import LOGGER_FORMAT, LOGGING_FILE

# Set up directories for logs
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logger
def setup_logger(name: str = "FLC", log_file: str = LOGGING_FILE, level: int = logging.INFO) -> logging.Logger:
    """
    Set up and configure a logger for the project.

    Parameters:
    - name (str): Name of the logger.
    - log_file (str): File where the logs will be saved.
    - level (int): Logging level. Defaults to INFO.

    Returns:
    - logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Formatter for logs
    formatter = logging.Formatter(
        LOGGER_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler with rotation (5 MB per file, 5 backup files)
    file_handler = RotatingFileHandler(os.path.join(LOG_DIR, log_file), maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # Stream (console) handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Adding handlers
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def get_logger_level(logger_level_str: str) -> int:
    """
    Get the logging level from a string.

    Parameters:
    - logger_level_str (str): String representation of the logging level.

    Returns:
    - int: Logging level.
    """
    level_map = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "NOTSET": logging.NOTSET,
    }
    
    logger_level = level_map.get(logger_level_str.upper())
    if logger_level is None:
        raise ValueError(f"Invalid log level: {logger_level_str}")
    
    return logger_level

# get logger
def get_logger(name: str = "FLC") -> logging.Logger:
    """
    Get a logger instance by name.

    Parameters:
    - name (str): Name of the logger.

    Returns:
    - logging.Logger: Logger instance.
    """
    return logging.getLogger(name)


class GUILogHandler(logging.Handler):
    """Logging handler that emits log messages to the GUI. Tight coupling with LogViewer.

    Parameters:
    - log_viewer (LogViewer): The LogViewer instance to emit logs to.
    - error_callback (Callable): Callback to notify of errors.
    """
    def __init__(self, log_viewer, error_callback):
        super().__init__()
        self.log_viewer = log_viewer
        self.error_callback = error_callback  # Callback to notify of errors

    def emit(self, record):
        """
        Called when a log event is emitted.
        """
        msg = self.format(record)
        level = record.levelname

        self.log_viewer.append_log(msg, level)

        # If an error occurs, trigger the error callback
        if level == "ERROR":
            self.error_callback()