import json
import sys
import boto3
import uuid
import os
from PIL import Image
from utils.image_utilities import *
from utils.aws_utilities import *

sg = boto3.client("sagemaker-runtime", region_name="us-east-1")

def handler(event, context = None):
    with Image.open(event["input_image_path"]) as pil_image:
        base64_im = pil_to_base64(pil_image)
        identifier = str(uuid.uuid4())
        input_location = f's3://{event["bucket_result_name"]}/{identifier}.json'
        with open(f"{identifier}.json", "w") as payload_file:
            json.dump(base64_im, payload_file)
            command = f'aws s3 cp ./{identifier}.json {input_location}'
            print(command)
            os.system(command)
        response = sg.invoke_endpoint_async(
            EndpointName = event["endpoint_name"],
            InputLocation = input_location,
            InferenceId = identifier,
            ContentType = "application/json"
        )
        print(response)
        print(json.dumps(response, indent=2))

def clean():
    os.system("rm *.json")

if __name__ == "__main__":
    print("Make a call to a sagemaker async endpoint")
    for i in range(20):
        handler({
            "endpoint_name": "nu0087002ei-aid-dev-firma-model",
            "bucket_result_name": "nu0087002ei-aid-dev-inference-results-bucket",
            "input_image_path": sys.argv[1]
        })
    clean()