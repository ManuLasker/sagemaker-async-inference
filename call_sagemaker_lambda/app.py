import json
import sys
import boto3
import uuid
import os
from PIL import Image
from src.utils.image_utilities import pil_to_base64 
from src.utils.aws_utilities import s3_check_to_download, s3_upload_file

sg = boto3.client("sagemaker-runtime", region_name="us-east-1")

def handler(event, context = None):
    with Image.open(event.get("input_image_path", "input/carta_laboral_image.jpg")) as pil_image:
        base64_im = pil_to_base64(pil_image)
        identifier = str(uuid.uuid4())
        bucket_name = event["bucket_result_name"]
        key = f'{identifier}.json'
        s3_upload_file(base64_im, bucket_name, key)
        response = sg.invoke_endpoint_async(
            EndpointName = event["endpoint_name"],
            InputLocation = f's3://{bucket_name}/{key}',
            InferenceId = identifier,
            ContentType = "application/json"
        )
        print(json.dumps(response))
        endpoint_result = s3_check_to_download(response["OutputLocation"])
        return endpoint_result

def clean():
    os.system("rm *.json")

if __name__ == "__main__":
    print("Make a call to a sagemaker async endpoint")
    handler({
        "endpoint_name": "nu0087002ei-aid-dev-firma-model",
        "bucket_result_name": "nu0087002ei-aid-dev-inference-results-bucket",
        "input_image_path": sys.argv[1]
    })
    clean()