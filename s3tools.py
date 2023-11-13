import typer
from s3helper import s3Helper
import sys

app = typer.Typer()
client = None


@app.command
def auth(access_token, secret):
    try:
        client = s3Helper(
            token=access_token,
            secret=secret
        )
    except Exception as e:
        print("Could not authenticate successfully ")


@app.command()
def upload(path: str, bucket: str, objectName: str = None):
    if client is None:
        print("Sorry, you have to authenticate first")
        sys.exit(1)
    client.upload(path, bucket, objectName)
    sys.exit(0)

@app.command()
def delete(bucket: str, objectKey: str = None):
    if client is None:
        print("Sorry, you have to authenticate first")
        sys.exit(1)
    client.delete(bucket, objectKey)

@app.command()
def create(name: str, acl: str):
    if client is None:
        print("Sorry, you have to authenticate first")
        sys.exit(1)
    client.createBucket(name,acl)

@app.command()
def list():
    if client is None:
        print("Sorry, you have to authenticate first")
        sys.exit(1)
    client.listBucket()
        


@app.command()
def create(name: str, acl: str):
    if client is None:
        print("Sorry, you have to authenticate first")
        sys.exit(1)


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()