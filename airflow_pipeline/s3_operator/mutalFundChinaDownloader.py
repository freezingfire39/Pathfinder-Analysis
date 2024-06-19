import os
import sys
# from airflow.exceptions import AirflowException
import boto3
from botocore.exceptions import NoCredentialsError
from pathlib import Path
home = str(Path.home())
# Usage
directory_path = home + '/Desktop/'  # Local directory to upload files from
bucket_name = 'mutal-fund-china-01'        # S3 bucket to upload to

'''def upload_files(directory, bucket_name):
    s3 = boto3.client('s3')
    try:
        # Walk through the directory
        for subdir, dirs, files in os.walk(directory): # travel dir tree
            for filename in files:
                # Construct the full local path
                local_path = os.path.join(subdir, filename)
                # Construct the full path for S3
                relative_path = os.path.relpath(local_path, directory)
                s3.upload_file(local_path, bucket_name, relative_path)
                print(f"Uploaded {relative_path} to {bucket_name}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(str(e))'''
def download_files(directory, bucket_name):
    s3 = boto3.client('s3')
    bucket_resources = boto3.resource('s3').Bucket(bucket_name)
    for obj in bucket_resources.objects.all():
        local_file_path = os.path.join(directory, obj.key)
        if not os.path.exists(os.path.dirname(local_file_path)):
            os.makedirs(os.path.dirname(local_file_path))
        s3.download_file(bucket_name, obj.key, local_file_path)
        print(f"Downloaded {obj.key} to {local_file_path}")

def main(downloadFilePath=None):
    if downloadFilePath != None:
        directory_path = downloadFilePath
    download_files(directory_path, bucket_name)
    pass
if __name__ == "__main__":
    # define data model here
    # pandas data frames, symbol, action, quantity
    # symbol and action must be upper case

    try:
        # main()
        downloadFilePath = sys.argv[1]
        main(downloadFilePath)
    except Exception as e:
        raise Exception("fail to run at error ", e)
    # main()
