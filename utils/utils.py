import logging
from boto3 import client

class Utils:

    # s3CopyFiles Constructor
    # logger: Logger object
    # config: Config Dict
    #
    # Returns: s3CopyFiles object
    # Raises: None
    def __init__(self, logger: logging.Logger, config: dict):

        self.logger = logger
        self.config = config

    # get_unique_dict_of_boto3_clients_from_config: Iterate through the config dictionary and build a unique dictionary of region names and their boto3 clients
    def get_unique_dict_of_boto3_clients_from_config(self, sub_config_list: list, unique_dict_of_boto3_clients: dict) -> dict:

        for source_bucket_region in sub_config_list:

            source_bucket_region_name = list(source_bucket_region.keys())[0]

            if source_bucket_region_name not in list(unique_dict_of_boto3_clients.keys()):

                self.logger.debug("Unique region - " + source_bucket_region_name)

                temp_client = client('s3', region_name=source_bucket_region_name)

                unique_dict_of_boto3_clients.update({source_bucket_region_name: temp_client})

        return unique_dict_of_boto3_clients