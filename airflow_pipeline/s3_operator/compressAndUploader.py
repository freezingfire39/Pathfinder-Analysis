import os
import sys
import zipfile
from airflow.exceptions import AirflowException
import boto3
from botocore.exceptions import NoCredentialsError
from pathlib import Path
import shutil

home = str(Path.home())
# Usage
directory_path = home + '/Desktop/'  # Local directory to upload files from
bucket_name = 'migration-bucket-21'  # S3 bucket to upload to


def zip_folder(folder_path, output_path):
    """
    Compress a folder into a zip file.

    Args:
        folder_path (str): Path to the folder to compress
        output_path (str): Path where the zip file should be created
    """
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add file to zip, preserving relative path structure
                    arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                    zipf.write(file_path, arcname)
        print(f"Successfully created zip archive at {output_path}")
        return True
    except Exception as e:
        print(f"Error creating zip archive: {str(e)}")
        return False


def upload_file_to_s3(file_path, bucket_name, s3_key=None):
    """
    Upload a single file to S3.

    Args:
        file_path (str): Local path to the file
        bucket_name (str): S3 bucket name
        s3_key (str): Key/path in S3 (if None, uses file name)
    """
    s3 = boto3.client('s3')
    try:
        if s3_key is None:
            s3_key = os.path.basename(file_path)
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_path} to {bucket_name}/{s3_key}")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        return False


def compress_and_upload_folders(folder_paths, bucket_name, cleanup=True):
    """
    Compress multiple folders and upload them to S3.

    Args:
        folder_paths (list): List of folder paths to compress and upload
        bucket_name (str): S3 bucket name
        cleanup (bool): Whether to delete the zip files after upload
    """
    for folder_path in folder_paths:
        if not os.path.isdir(folder_path):
            print(f"Skipping {folder_path} - not a directory")
            continue

        # Create zip file in the same directory as the folder
        folder_name = os.path.basename(folder_path.rstrip('/'))
        zip_filename = f"{folder_name}.zip"
        zip_path = os.path.join(os.path.dirname(folder_path), zip_filename)

        # Compress the folder
        if zip_folder(folder_path, zip_path):
            # Upload the zip file
            if upload_file_to_s3(zip_path, bucket_name):
                print(f"Successfully uploaded {folder_name} as {zip_filename}")
                # Clean up the zip file if requested
                if cleanup:
                    try:
                        os.remove(zip_path)
                        print(f"Removed temporary zip file {zip_path}")
                    except Exception as e:
                        print(f"Error removing zip file: {str(e)}")


def main(upload_file_paths=None):
    if upload_file_paths is not None:
        if isinstance(upload_file_paths, str):
            # Handle single path or comma-separated list
            paths = [path.strip() for path in upload_file_paths.split(',')]
        else:
            paths = upload_file_paths
        compress_and_upload_folders(paths, bucket_name)
    else:
        print("No folders specified for compression and upload")

# how to run:
# python compressAndUploader.py "/path/to/folder1,/path/to/folder2"
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            upload_file_paths = sys.argv[1]
            main(upload_file_paths)
        else:
            print("Please provide folder paths to compress and upload")
    except Exception as e:
        raise AirflowException("Failed to run with error: ", e)