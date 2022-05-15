import boto3
import io
import json
import urllib
import botocore
import time

s3 = boto3.client('s3')
time_limit = 15 * 60 # 15 minutes of timeout

def s3_upload_file(data: str, bucket_name: str, key: str):
    """upload string data to a json file in a target bucket

    Args:
        data (str): String to upload to some file
        bucket_name (str): Bucket name where we want to upload the file
        key (str): Target's name where data will be saved
    """
    with io.BytesIO(json.dumps(data).encode()) as f:
        s3.upload_fileobj(f, bucket_name, key)

def s3_check_to_download(s3_result_path: str):
    """check if request is already processed and download the endpoint's result

    Args:
        s3_result_path (str): s3 uri to result path
    """
    output_url = urllib.parse.urlparse(s3_result_path)
    bucket = output_url.netloc
    key = output_url.path[1:]

    init_time = time.time()
    while True and time.time() - init_time <= time_limit:
        try:
            with io.BytesIO() as f:
                s3.download_fileobj(bucket, key, f)
                return json.loads(f.read().decode())
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'NoSuchKey':
                print('waiting for output to be processed')
                time.sleep(2)
                continue
            raise Exception(f'There was an error searching for results in bucket: {bucket}'
                            f', error: {error}'
                            f', key: {key}')
    raise Exception(f'Timeout Exception, waiting time excedded, time limit {time_limit}')