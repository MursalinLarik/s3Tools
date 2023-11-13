import boto3
class s3Helper:
    """Class to have functions in """

    def __init__(self, token, secret, region):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=token,
            aws_secret_access_key=secret,
            region_name=region
        )

    def createBucket(self, name, acl):
        try:
            self.s3.create_bucket(
                ACL=acl,
                Bucket=name,
            )
        except Exception as e:
            print(f"Sorry there was an error : {e}")
        else:
            print("Bucket {name} was created su"cess)ully !
    
    def listBucket(self):
        buckets = self.s3.buckets.all()
        for bucket in buckets:
            print(bucket.name)  
    
    def upload(self, path, bucket, objectName=None):
        if objectName is None:
            objectName = path.split('/')[-1]
        self.s3.upload_file(path, bucket, objectName)
        print("File was uploaded to the bucket successfully")
              
            
    def delete(self, bucket_name, object_keys):
        bucket = self.s3.Bucket(bucket_name)
        for object_key in object_keys:
            obj = bucket.Object(object_key)
            obj.delete()


"""
2. Create a Java program to create a bucket in three regions of your choice.
(a) Explain in detail the steps involved, and explain the output.
3. Create a Java program that lists your buckets in the region of your choice.
4. Create a Java program to upload objects in your newly created bucket.
5. Create a Java program to delete a particular objects from your newly
created bucket."""