import os
import yaml
import logging
import logging.config


def setup_logging(config_path: str = './auto_report_writer/configs/logger_config.yaml',
                  default_level: int = logging.INFO) -> None:
    """
    Sets up logging configuration.

    :param config_path: (str) Path to the logging configuration file (YAML format).
    :param default_level: (int) Default logging level if config file is not found or fails to load.
    """
    if os.path.exists(config_path):  # If the file exists at the specified config_path...
        try:
            # Opens the YAML configuration file as read-only.
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)  # Loads the YAML configuration.
            logging.config.dictConfig(config)  # Configures the logging with the loaded configuration.

        except yaml.YAMLError as e:  # For if there is an expected error in the YAML configuration file.
            logging.basicConfig(level=default_level)
            logging.error(f"Error parsing YAML file: {e}"
                          f"\nDefault logger initialised.")

        except Exception as e:  # For if there is an unexpected error in the YAML configuration file.
            logging.basicConfig(level=default_level)
            logging.error(f"Unexpected error reading logging configuration: {e}"
                          f"\nDefault logger initialised.")

    else:  # If the file at the specified config_path could not be found...
        logging.basicConfig(level=default_level)
        logging.error(f"Logging configuration file not found: {config_path}"
                      f"\nDefault logger initialised.")


# Calls the setup_logging function to configure logging.
setup_logging()

# Creates the logger instances.
app_logger = logging.getLogger('logger')  # Main application logger.
dev_logger = logging.getLogger('dev_logger')  # Development-specific logger.

# Sets the default logger to application logger.
logger = app_logger  # Change to dev_logger as needed for detailed logging.
