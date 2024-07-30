import logging
import logging.config
import os
import json


def setup_logging(config_path='./auto_report_writer/configs/logger_config.json',
                  default_level=logging.INFO):
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)  # Load the JSON configuration
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


# Call the setup_logging function to configure logging
setup_logging()

# Create a logger instance
logger = logging.getLogger('my_logger')


# Helper functions to log messages
def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)


def log_warning(message):
    logger.warning(message)
