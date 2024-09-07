from os import environ, getcwd, listdir
import logging
import traceback
import json

# ConfigHandler: class to handle configuration file
class ConfigHandler():

    # ConfigHandler Constructor
    #
    # Returns: ConfigHandler object
    # Raises: None
    def __init__(self, logger: logging.Logger):

        # Create a JSON Config parser
        self.logger = logger
        self.required_fields = ['srcBucket', 'dstBucket']

    # get_boolean: Takes a strings, returns bool
    def get_boolean(self, key: str) -> bool:
        return True if str(key).lower() == 'true' and key != '' else False

    # __load_config_file: Load the config.json file from the current working directory, returns dict
    def __load_config_file(self) -> dict:

        try:
            config = {}
            local_directory = getcwd()

            if 'GITHUB_ACTIONS' in environ.keys():

                self.logger.debug('Running inside GitHub Actions')
                local_directory = environ.get('GITHUB_WORKSPACE')

            for file in listdir(local_directory):

                if file == 'config.json':

                    with open('config.json', 'r+') as config_file:

                        config = json.loads(config_file.read())

                        self.logger.debug("JSON Config - " + str(config))

            return config if config else self.config
        
        except Exception as e:
            self.logger.error('Error loading config.json file: ' + str(traceback.print_tb(e.__traceback__)))
            
    # get_combined_config: Get combined config from config file and environment variables, returns dict
    def get_combined_config(self) -> dict:

        try:
            # Build a config file using config.json if it exists
            return self.__load_config_file()

        except Exception as e:
            self.logger.error('Error merging config: ' + str(traceback.print_tb(e.__traceback__)))
        