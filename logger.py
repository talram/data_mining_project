import logging
import sys


class Logger:
    def __init__(self):
        # Initiate the logger object
        self.logger = logging.getLogger(__name__)

        # Set the level of the logger
        self.logger.setLevel(logging.DEBUG)

        # Create the logs.log file
        handler = logging.FileHandler('logs.log')

        # Format the logs structure so that every line would include the time, name, level name and log message
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the format handler
        self.logger.addHandler(handler)

        # Print the logs to the console
        self.logger.addHandler(logging.StreamHandler(sys.stdout))


logger = Logger().logger
