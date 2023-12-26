import logging


def configure_logger():
    """
    Configures the logger for the application.
    This function sets up the logging module to log messages to a file called 'atm_log.txt'. The log level is set to
    DEBUG, which means that all log messages, including debug, info, warning, error, critical messages, will be logged.
    The log messages are formatted with the current time, the log level, and the log message itself.
    """
    logging.basicConfig(filename="atm_log.txt", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
