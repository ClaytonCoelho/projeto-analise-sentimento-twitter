import logging
import boto3
from botocore.exceptions import ClientError
import os

class AWSS3:
    def __init__(self):
        self.__aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        self.__aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=self.__aws_access_key_id,
                                      aws_secret_access_key=self.__aws_secret_access_key)

    def upload_file(self, file_name, bucket, path, object_name=None):
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name
        # Upload the file
        try:
            response = self.s3_client.upload_file(path + file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download_file(self, file_name, bucket, path, object_name=None):
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name
        # Download the file
        try:
            response = self.s3_client.download_file(bucket, object_name, path + file_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

