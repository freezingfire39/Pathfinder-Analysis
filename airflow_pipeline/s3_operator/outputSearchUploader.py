import os
import sys
from airflow.exceptions import AirflowException
import boto3
from botocore.exceptions import NoCredentialsError
from pathlib import Path
home = str(Path.home())
# Usage
directory_path = home + '/Desktop/'  # Local directory to upload files from
bucket_name = 'search-filter-china'        # S3 bucket to upload to

def upload_files(directory, bucket_name):
    s3 = boto3.client('s3')
    try:
        # Walk through the directory
        # for subdir, dirs, files in os.walk(directory): # travel dir tree
            for filename in os.listdir(directory):
                # Construct the full local path
                local_path = os.path.join(directory, filename)
                # Construct the full path for S3
                # relative_path = os.path.relpath(local_path, directory)
                s3.upload_file(local_path, bucket_name, filename)
                print(f"Uploaded {filename} to {bucket_name}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(str(e))

def main(uploadFilePath=None):
    if uploadFilePath != None:
        directory_path = uploadFilePath
    upload_files(directory_path, bucket_name)
    pass
if __name__ == "__main__":
    # define data model here
    # pandas data frames, symbol, action, quantity
    # symbol and action must be upper case

    try:
        # main()
        uploadFilePath = sys.argv[1]
        main(uploadFilePath)
    except Exception as e:
        raise AirflowException("fail to run at error ", e)
    # main()
