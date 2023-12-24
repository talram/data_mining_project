import json
import os

from general.logger import logger


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    try:
        with open(config_path, 'r') as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        logger.error("config.json file not found.")
        return None
    except json.JSONDecodeError:
        logger.error("Error decoding JSON in config.json.")
        return None


def load_constants():
    config_data = load_config()
    if config_data is not None:
        return config_data.get('constants', {})
    else:
        return {}


def load_db_config():
    config_data = load_config()

    if config_data is not None:
        logger.info("\n*** Database configurations are loaded and ready to use. ***\n")
        return config_data.get('DB_CONFIG', {})
    else:
        return {}
