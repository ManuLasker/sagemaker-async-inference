import boto3
import io
import json

s3 = boto3.client('s3')

def s3_upload_file(data: str, bucket_name: str, key: str):
    """upload string data to a json file in a target bucket

    Args:
        data (str): String to upload to some file
        bucket_name (str): Bucket name where we want to upload the file
        key (str): Target's name where data will be saved
    """
    with io.BytesIO(json.dumps(data).encode()) as f:
        s3.upload_fileobj(f, bucket_name, key)

def s3_check_to_download(file_name: str, bucket_name: str):
    