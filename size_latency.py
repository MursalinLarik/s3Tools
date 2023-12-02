import boto3
import time
from io import BytesIO

import json

creds = json.loads(open("credentials.json").read())

# Replace these with your AWS credentials and bucket information
ACCESS_KEY = creds["access_token"]
SECRET_KEY = creds["secret"]
BUCKET_NAME = "muhmoh-bucket2-lab1"
# REGION_NAMES = ["us-east-1", "us-west-2", "eu-west-1"]
REGION_NAMES = "us-west-1"

def create_test_data(size_mb):
    # Create a BytesIO object with random data of the specified size
    return BytesIO(b"0" * (size_mb * 1024 * 1024))

def upload_object(s3_client, bucket_name, object_key, data):
    # Upload the object to the specified S3 bucket
    start_time = time.time()
    s3_client.upload_fileobj(data, bucket_name, object_key)
    end_time = time.time()
    return end_time - start_time

def download_object(s3_client, bucket_name, object_key):
    # Download the object from the specified S3 bucket
    start_time = time.time()
    s3_client.download_file(bucket_name, object_key, "/dev/null")
    end_time = time.time()
    return end_time - start_time

def main():
    # Create an S3 client
    for region_name in REGION_NAMES:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name=region_name
        )

        for size_mb in [1, 10, 100]:
            object_key = f"test_object_{size_mb}mb.txt"
            data = create_test_data(size_mb)

            # Upload the object and measure the latency
            upload_latency = upload_object(s3_client, BUCKET_NAME, object_key, data)
            print(f"Upload Latency ({size_mb} MB) in {region_name}: {upload_latency:.4f} seconds")

            # Download the object and measure the latency
            download_latency = download_object(s3_client, BUCKET_NAME, object_key)
            print(f"Download Latency ({size_mb} MB) in {region_name}: {download_latency:.4f} seconds")

if __name__ == "__main__":
    main()
