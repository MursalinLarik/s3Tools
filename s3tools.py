import typer
from s3helper import S3Helper
import sys
import json

creds = json.loads(open("credentials.json").read())

app = typer.Typer()
client = S3Helper(
    token=creds["access_token"], secret=creds["secret"], region=creds["region"]
)

if client is None:
    print("Sorry, you have to provide a credentials.json file to authenticate")
    sys.exit(1)


@app.command()
def upload(path: str, bucket: str, object_name: str):
    client.upload(path, bucket, object_name)
    sys.exit(0)


@app.command()
def delete(bucket: str, object_key: str):
    client.delete_objects(bucket, [object_key])


@app.command()
def create(name: str, acl: str):
    client.create_bucket(name, acl)


@app.command()
def list():
    buckets = client.list_buckets()
    for bucket in buckets:
        print(bucket)


if __name__ == "__main__":
    app()
