import os
import yaml
import logging
import logging.config


def setup_logging(config_path='./auto_report_writer/configs/logger_config.yaml',
                  default_level=logging.INFO):
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)  # Load the YAML configuration
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()  # Call the setup_logging function to configure logging
app_logger = logging.getLogger('logger')
dev_logger = logging.getLogger('dev_logger')

# Change to 'dev_logger' for more detailed logs.
logger = app_logger
