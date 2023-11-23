import boto3


class S3Helper:
    """Class to have functions in"""

    def __init__(self, token, secret, region):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=token,
            aws_secret_access_key=secret,
            region_name=region,
        )

    def create_bucket(self, name, acl=None):
        if acl is None:
            print(
                "ACL cannot be None; it has to be one of these values: 'private'|'public-read'|'public-read-write'|'authenticated-read'"
            )
            return

        try:
            self.s3.create_bucket(
                ACL=acl,
                Bucket=name,
            )
        except Exception as e:
            print(f"Sorry, there was an error: {e}")
        else:
            print(f"Bucket {name} was created successfully!")

    def list_buckets(self):
        response = self.s3.list_buckets()
        return [bucket["Name"] for bucket in response["Buckets"]]

    def upload(self, path, bucket, object_name):
        if object_name is None:
            object_name = path.split("/")[-1]
        try:
            self.s3.upload_file(path, bucket, object_name)
            print("File was uploaded to the bucket successfully")
        except Exception as e:
            print(f"Sorry, there was an error uploading the file: {e}")

    def delete_objects(self, bucket_name, object_keys):
        try:
            self.s3.delete_objects(
                Bucket=bucket_name,
                Delete={"Objects": [{"Key": key} for key in object_keys]},
            )
            print("Objects deleted successfully")
        except Exception as e:
            print(f"Sorry, there was an error deleting objects: {e}")
