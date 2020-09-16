import boto3
import os

class AWSDynamoDB:
    def __init__(self):
        self.__aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        self.__aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        self.dynamodb_client = boto3.client(
            'dynamodb',
            region_name="us-east-1",
            aws_access_key_id=self.__aws_access_key_id,
            aws_secret_access_key=self.__aws_secret_access_key)

    def put_item(self, item, table_name):
        response = self.dynamodb_client.put_item(
            TableName = table_name,
            Item = item
        )

        return response
