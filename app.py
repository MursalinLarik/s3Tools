import streamlit as st
import os
from s3helper import S3Helper
import json

creds = json.loads(open("credentials.json").read())

s3 = S3Helper(
    token=creds["access_token"], secret=creds["secret"], region=creds["region"]
)


def main():
    st.title("S3 Manager")

    # List available buckets in a dropdown
    buckets = s3.list_buckets()
    selected_bucket = st.selectbox("Select S3 Bucket", buckets)

    uploaded_file = st.file_uploader("Choose a file")

    if st.button("Upload to S3") and uploaded_file is not None:
        try:
            # Save the file to a temporary location
            temp_file_path = os.path.join("/tmp", uploaded_file.name)
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.read())

            # Upload the file to S3 using the temporary file path
            s3.upload(
                path=temp_file_path,
                bucket=selected_bucket,
                object_name=uploaded_file.name,
            )
        except Exception as e:
            st.error(f"Cannot upload file: {e}")
        else:
            st.success("File uploaded successfully!")


if __name__ == "__main__":
    main()
