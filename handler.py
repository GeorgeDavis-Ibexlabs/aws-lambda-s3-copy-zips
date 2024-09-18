import logging
from os import environ
import traceback
import boto3

# Setting up the logging level from the environment variable `LOGLEVEL`.
if 'LOG_FILENAME' in environ.keys():
    logging.basicConfig(
        filename=environ['LOG_FILENAME'],
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S'
    )
    logger = logging.getLogger(__name__)
else:
    logging.basicConfig()
    logger = logging.getLogger(__name__)

logger.setLevel(environ['LOGLEVEL'] if 'LOGLEVEL' in environ.keys() else 'INFO')

# Setting up logging level specific to `botocore` from the environment variable `BOTOCORE_LOGLEVEL`.
if 'BOTOCORE_LOGLEVEL' in environ.keys():
    if environ['BOTOCORE_LOGLEVEL'] == 'DEBUG':    
        logger.info('Setting boto3 logging to DEBUG')
        boto3.set_stream_logger('') # Log everything on boto3 messages to stdout
    else:
        logger.info('Setting boto3 logging to ' + environ['BOTOCORE_LOGLEVEL'])
        boto3.set_stream_logger(level=logging._nameToLevel[environ['BOTOCORE_LOGLEVEL']]) # Log boto3 messages that match BOTOCORE_LOGLEVEL to stdout

from config_handler.config_handler import ConfigHandler
config_handler = ConfigHandler(logger=logger)
config = config_handler.get_config()
logger.debug("Final config - " + str(config))

from utils.utils import Utils
utils = Utils(logger=logger, config=config)

from s3.s3 import s3CopyFiles
s3_copy_files = s3CopyFiles(logger=logger, config=config)

# main: This script executes as a Custom Resource to copy files across S3 buckets and regions. The script is executed if the stack was created, updated or removed.
def main():

    logger.debug('Environment variables - ' + str(environ))
    logger.debug("Config - " + str(config))

    try:

        if config is not None:

            dict_of_boto3_clients = {}
            dict_of_boto3_clients.update(
                utils.get_unique_dict_of_boto3_clients_from_config(
                    sub_config_list=config["srcBucket"],
                    unique_dict_of_boto3_clients=dict_of_boto3_clients
                )
            )        
            # dict_of_boto3_clients.update(
            #     utils.get_unique_dict_of_boto3_clients_from_config(
            #         sub_config_list=config["dstBucket"],
            #         unique_dict_of_boto3_clients=dict_of_boto3_clients
            #     )
            # )
            logger.debug("Dictionary of boto3 clients for source regions to initiate copy_object - " + str(dict_of_boto3_clients))

            for src_bucket_region in config["srcBucket"]:

                src_bucket_region_name = list(src_bucket_region.keys())[0]
                logger.debug("Creating a boto3 client for " + src_bucket_region_name)

                for src_bucket in src_bucket_region[src_bucket_region_name]:

                    logger.debug("Source S3 Bucket: " + src_bucket["s3Bucket"])

                    for s3_object in src_bucket["objects"]:

                        if s3_copy_files.check_s3_object_exists(
                            s3_client=dict_of_boto3_clients[src_bucket_region_name],
                            bucket_name=src_bucket["s3Bucket"],
                            object_key=s3_object["s3KeyPrefix"] + s3_object["s3Key"]
                        ):
                            logger.info("Object " + s3_object["s3Key"] + " exists.")

                            for dst_bucket_region in config["dstBucket"]:

                                dst_bucket_region_name = list(dst_bucket_region.keys())[0]

                                for dst_bucket in dst_bucket_region[dst_bucket_region_name]:

                                    logger.debug("Destination S3 Bucket: " + dst_bucket["s3Bucket"])

                                    logger.info("Copying " + s3_object["s3KeyPrefix"] + s3_object["s3Key"] + " from " + src_bucket["s3Bucket"] + " to " + dst_bucket["s3Bucket"])

                                    s3_copy_files.s3_copy(
                                        s3_client=dict_of_boto3_clients[src_bucket_region_name],
                                        src_bucket=src_bucket["s3Bucket"],
                                        src_key=s3_object["s3KeyPrefix"] + s3_object["s3Key"],
                                        dst_bucket=dst_bucket["s3Bucket"],
                                        dst_key=s3_object["s3KeyPrefix"] + s3_object["s3Key"]
                                    )

                        else:
                            logger.error("Object " + s3_object["s3Key"] + " does not exist.")

    except Exception as e:
        logger.exception("Unhandled Error: " + str(traceback.print_tb(e.__traceback__)))
        raise

if __name__ == '__main__':
    main()