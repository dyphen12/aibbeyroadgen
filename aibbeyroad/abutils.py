"""

abutils.py

This module contains a number of utility functions for use with the Aibbey Road project.

"""

import logging
import boto3
from botocore.exceptions import ClientError
import os
import json


class awsconfig:
    def __init__(self, bucket, folder, bars):
        self.bucket = bucket
        self.folder = folder
        self.bars = bars


def load_config():
    config_loc = 'awsconfig.json'
    try:
        with open(config_loc) as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
            print(jsonObject)

            awsc = awsconfig(jsonObject['bucket'], jsonObject['folder'], jsonObject['bars'])

        return awsc

    except FileNotFoundError:
        print('Config not found.')

# Upload file to an s3 bucket
def upload_file(file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)


    #upload file to folder in bucket



    # Upload the file
    s3_client = boto3.client('s3')

    s3config = load_config()

    s3folder = s3config.folder + '/{}'

    print(s3folder)


    try:
        response = s3_client.upload_file(file_name, s3config.bucket, s3folder.format(object_name))

    except ClientError as e:
        logging.error(e)
        return False
    return True



def get_buckets():
    # Let's use Amazon S3
    s3 = boto3.resource("s3")

    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)