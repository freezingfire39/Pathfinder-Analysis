import os
import sys
import boto3
from botocore.exceptions import NoCredentialsError
from pathlib import Path
home = str(Path.home())
# Usage
directory_path = home + '/Desktop/'  # Local directory to upload files from
bucket_name = 'search-filter-china'        # S3 bucket to upload to


def download_files(bucket_name, local_directory):
    s3 = boto3.client('s3')
    try:
        # List all objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name)

        # Check if the bucket has any contents
        if 'Contents' in response:
            for item in response['Contents']:
                file_name = item['Key']
                local_path = os.path.join(local_directory, file_name)

                # Create subdirectory structure if it does not exist
                if not os.path.exists(os.path.dirname(local_path)):
                    os.makedirs(os.path.dirname(local_path))

                # Download the file
                s3.download_file(bucket_name, file_name, local_path)
                print(f"Downloaded {file_name} to {local_path}")
        else:
            print("No files found in the bucket.")

    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(str(e))



local_directory = '/home/app/Desktop/output_search'
download_files(bucket_name, local_directory)