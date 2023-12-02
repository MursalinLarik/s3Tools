import time
from s3helper import S3Helper
import json
import csv


def measure_latency(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        latency = end_time - start_time
        print(f"Latency: {latency:.5f} seconds")
        return latency

    return wrapper


@measure_latency
def upload_to_s3(file_path, bucket_name, object_key):
    s3_helper.upload(file_path, bucket_name, object_key)


@measure_latency
def download_from_s3(bucket_name, object_key, local_file_path):
    s3_helper.download(local_file_path, bucket_name, object_key)


creds = json.loads(open("credentials.json").read())

s3_helper = S3Helper(
    token=creds["access_token"], secret=creds["secret"], region=creds["region"]
)

# Specify the local files and S3 object keys
files_to_upload = [
    "1MB_file.txt",
    "10MB_file.txt",
    "50MB_file.txt",
    "100MB_file.txt",
    "500MB_file.txt",
    "1000MB_file.txt",
]
s3_object_keys = [
    "1MB_object",
    "10MB_object",
    "50MB_object",
    "100MB_object",
    "500MB_object",
    "1000MB_object",
]

bucket_name = "muhmoh-lab1"

# Store latency information in a CSV file
csv_file_path = "latency_results.csv"
with open(csv_file_path, mode="w", newline="") as csv_file:
    fieldnames = ["Operation", "File Size (MB)", "Latency (seconds)"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Upload files to S3 and record latency
    for local_file, object_key in zip(files_to_upload, s3_object_keys):
        latency = upload_to_s3("objects/" + local_file, bucket_name, object_key)
        writer.writerow(
            {
                "Operation": "Upload",
                "File Size (MB)": local_file.replace("MB_file.txt", ""),
                "Latency (seconds)": latency,
            }
        )

    # Download files from S3 and record latency
    for local_file, object_key in zip(files_to_upload, s3_object_keys):
        latency = download_from_s3(bucket_name, object_key, f"downloaded_{local_file}")
        writer.writerow(
            {
                "Operation": "Download",
                "File Size (MB)": local_file.replace("MB_file.txt", ""),
                "Latency (seconds)": latency,
            }
        )
