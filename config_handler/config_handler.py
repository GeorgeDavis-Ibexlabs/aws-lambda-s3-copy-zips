from os import environ, getcwd, listdir
import logging
import traceback
import json

# ConfigHandler: class to handle configuration file and configuration environment variables
class ConfigHandler():

    # ConfigHandler Constructor
    #
    # Returns: ConfigHandler object
    # Raises: None
    def __init__(self, logger: logging.Logger):

        # Create a JSON Config parser
        self.logger = logger
        self.required_fields = ['srcBucket', 'dstBucket']
        self.required_env_vars = ['SRC_REGION', 'SRC_BUCKET', 'SRC_KEY_PREFIX', 'SRC_KEY', 'DST_REGION', 'DST_BUCKET']
        self.required_env_vars_dict = {
            'INPUT_SRC_REGION': 'SRC_REGION',
            'INPUT_SRC_BUCKET': 'SRC_BUCKET',
            'INPUT_SRC_KEY_PREFIX': 'SRC_KEY_PREFIX',
            'INPUT_SRC_KEY': 'SRC_KEY',
            'INPUT_DST_REGION': 'DST_REGION',
            'INPUT_DST_BUCKET': 'DST_BUCKET'
        }

    # get_boolean: Takes a strings, returns bool
    def get_boolean(self, key: str) -> bool:
        return True if str(key).lower() == 'true' and key != '' else False

    # Build the Config object
    def build_config(self, config_dict: dict) -> dict:

        self.logger.debug('Config Dict - ' + str(config_dict))
        return {
            'srcBucket': [
                {
                    config_dict['SRC_REGION']: [
                        {
                            's3Bucket':  config_dict['SRC_BUCKET'],
                            'objects': [
                                {
                                    's3KeyPrefix': config_dict['SRC_KEY_PREFIX'],
                                    's3Key': config_dict['SRC_KEY']
                                }
                            ]
                        }
                    ]
                }
            ],
            'dstBucket': [
                {
                    config_dict['DST_REGION']: [
                        {
                            's3Bucket': config_dict['DST_BUCKET']
                        }
                    ]
                }
            ]
        }
    
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

            return config
        
        except Exception as e:
            self.logger.error('Error loading config.json file: ' + str(traceback.print_tb(e.__traceback__)))
            
    # __load_config_env: Load the config.json file from environment variables instead if running inside GitHub Actions. Environment variables override config.json values to enable CI workflows.
    def __load_config_env(self) -> dict:

        try:
            temp_dict = {}
            for config_key in self.required_env_vars:

                self.logger.debug('config_key - ' + str(config_key))
        
                if 'GITHUB_ACTIONS' in environ.keys():
                    if environ['GITHUB_ACTIONS']:
                        config_key = 'INPUT_' + config_key

                self.logger.debug("Final config_key based on runtime environment - " + str(config_key))

                if config_key in environ.keys():
                    self.logger.debug('Config found within environment variables - ' + str(config_key))

                    if 'GITHUB_ACTIONS' in environ.keys():
                        if environ['GITHUB_ACTIONS']:
                            temp_dict.update({self.required_env_vars_dict[config_key]: environ.get(config_key)})
                    else:
                        temp_dict.update({config_key: environ.get(config_key)})

                # elif 'DST_REGION' in config_key:
                #     self.logger.info('Missing environment variable DST_REGION. Substituting SRC_REGION in place of DST_REGION.')
                #     if 'SRC_REGION' in temp_dict:
                #         temp_dict.update({config_key: temp_dict['SRC_REGION']})
                #     elif 'SRC_REGION' in environ.keys():
                #         temp_dict.update({config_key: environ.get('SRC_REGION')})
                #     else:
                #         self.logger.error('Missing SRC_REGION within environment variables')
                #         raise

                else:                    
                    if 'GITHUB_ACTIONS' in environ.keys():
                        if environ['GITHUB_ACTIONS']:
                            self.logger.error('Missing ' + self.required_env_vars_dict[config_key] + ' within environment variables')    
                    else:                        
                        self.logger.debug('Missing ' + config_key + ' within environment variables')
                    raise RuntimeError                

            config_dict = self.build_config(config_dict=temp_dict)

            self.logger.debug('ConfigMap JSON key values found within environment variables - ' + str(config_dict))

            return config_dict
        
        except RuntimeError as runtime_err:
            self.logger.error('Missing environment variable: ' + str(traceback.print_tb(runtime_err.__traceback__)))

        except Exception as e:
            self.logger.error('Error loading environment variables: ' + str(traceback.print_tb(e.__traceback__)))
            
    # get_combined_config: Get config from config file. If empty, check for config within environment variables. Returns dict
    def get_combined_config(self) -> dict:

        try:
            # Build a config file using config.json if it exists    
            config = self.__load_config_file()

            # Override config.json if exists, with Environment variables for CI purposes
            if not config:
                config = self.__load_config_env()

            if not config:
                self.logger.error('Config Error: No configuration found within config files and environment variables.')

            return config

        except Exception as e:
            self.logger.error('Error reading config: ' + str(traceback.print_tb(e.__traceback__)))