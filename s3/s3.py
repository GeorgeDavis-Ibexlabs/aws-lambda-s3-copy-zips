import logging
from boto3 import client
from botocore.exceptions import ClientError

class s3CopyFiles:

    # s3CopyFiles Constructor
    # logger: Logger object
    # config: Config Dict
    #
    # Returns: s3CopyFiles object
    # Raises: None
    def __init__(self, logger: logging.Logger, config: dict):

        self.logger = logger
        self.config = config

    # check_s3_object_exists: Check if a file exists on an S3 bucket, returns `bool`. 
    def check_s3_object_exists(self, s3_client: client, bucket_name: str, object_key: str) -> bool:
            
        try:            
            s3_client.head_object(Bucket=bucket_name, Key=object_key)
            return True
        
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise

    # s3_copy: Copy S3 object from source to destination bucket
    def s3_copy(self, s3_client: client, src_bucket: str, src_key: str, dst_bucket: str, dst_key: str) -> bool:

        # Boto3 copy_object
        s3_client.copy_object(
            Bucket=dst_bucket,
            Key=dst_key,
            CopySource={'Bucket': src_bucket, 'Key': src_key}
        )

        self.logger.info("Copy complete.")

