import os
import zipfile
import boto3
from botocore.exceptions import NoCredentialsError
from pathlib import Path
import tempfile

home = str(Path.home())
bucket_name = 'mutal-fund-china-01'  # Same bucket as before


def download_from_s3(bucket_name, s3_key, local_path):
    """
    Download a file from S3 to a local path.

    Args:
        bucket_name (str): S3 bucket name
        s3_key (str): Key/path of the file in S3
        local_path (str): Local path to save the file to
    """
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, s3_key, local_path)
        print(f"Downloaded {s3_key} to {local_path}")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"Error downloading from S3: {str(e)}")
        return False


def unzip_file(zip_path, extract_to=None):
    """
    Unzip a file to a specified directory.

    Args:
        zip_path (str): Path to the zip file
        extract_to (str): Directory to extract to (default: same directory as zip file)
    """
    if extract_to is None:
        extract_to = os.path.dirname(zip_path)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted {zip_path} to {extract_to}")
        return True
    except Exception as e:
        print(f"Error extracting zip file: {str(e)}")
        return False


def download_and_extract(bucket_name, s3_keys, download_dir=None, keep_zips=False):
    """
    Download and extract zip files from S3.

    Args:
        bucket_name (str): S3 bucket name
        s3_keys (list): List of S3 keys (paths) to download
        download_dir (str): Local directory to download to (default: temp directory)
        keep_zips (bool): Whether to keep the zip files after extraction
    """
    if download_dir is None:
        download_dir = tempfile.mkdtemp()
        print(f"Using temporary directory: {download_dir}")

    if isinstance(s3_keys, str):
        s3_keys = [s3_keys]

    for s3_key in s3_keys:
        if not s3_key.endswith('.zip'):
            print(f"Skipping {s3_key} - not a zip file")
            continue

        # Download the zip file
        zip_filename = os.path.basename(s3_key)
        local_zip_path = os.path.join(download_dir, zip_filename)

        if download_from_s3(bucket_name, s3_key, local_zip_path):
            # Extract the zip file
            extract_path = os.path.join(download_dir, os.path.splitext(zip_filename)[0])
            os.makedirs(extract_path, exist_ok=True)

            if unzip_file(local_zip_path, extract_path):
                print(f"Successfully extracted {s3_key} to {extract_path}")
                # Remove zip file if not keeping it
                if not keep_zips:
                    try:
                        os.remove(local_zip_path)
                        print(f"Removed zip file {local_zip_path}")
                    except Exception as e:
                        print(f"Error removing zip file: {str(e)}")
            else:
                print(f"Failed to extract {s3_key}")


def list_zip_files_in_bucket(bucket_name, prefix=''):
    """
    List all zip files in the specified bucket with optional prefix.

    Args:
        bucket_name (str): S3 bucket name
        prefix (str): Only list keys starting with this prefix
    """
    s3 = boto3.client('s3')
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        zip_files = []

        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'].endswith('.zip'):
                    zip_files.append(obj['Key'])

        return zip_files
    except Exception as e:
        print(f"Error listing bucket contents: {str(e)}")
        return []


def main_download(s3_keys=None, download_dir=None, keep_zips=False):
    """
    Main function for download and extract operations.

    Args:
        s3_keys (str/list): Either a single key, comma-separated keys, or None to list all zips
        download_dir (str): Directory to download to (default: temp directory)
        keep_zips (bool): Whether to keep zip files after extraction
    """
    if s3_keys is None:
        # List all zip files in bucket and let user choose
        zip_files = list_zip_files_in_bucket(bucket_name)
        if not zip_files:
            print("No zip files found in bucket")
            return

        print("Available zip files in bucket:")
        for i, zip_file in enumerate(zip_files, 1):
            print(f"{i}. {zip_file}")

        selection = input("Enter numbers to download (comma-separated) or 'all': ")
        if selection.lower() == 'all':
            s3_keys = zip_files
        else:
            try:
                selected_indices = [int(x.strip()) for x in selection.split(',')]
                s3_keys = [zip_files[i - 1] for i in selected_indices]
            except (ValueError, IndexError):
                print("Invalid selection")
                return
    elif isinstance(s3_keys, str):
        s3_keys = [key.strip() for key in s3_keys.split(',')]

    download_and_extract(bucket_name, s3_keys, download_dir, keep_zips)

# Download specific files:
# python download_script.py --keys "folder1.zip,folder2.zip" --dir ~/Downloads
# Interactive mode (list and choose files):
# python download_script.py
# Keep zip files after extraction:
# python download_script.py --keys "data.zip" --keep-zips
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Download and extract zip files from S3')
    parser.add_argument('--keys', type=str, help='Comma-separated S3 keys to download')
    parser.add_argument('--dir', type=str, help='Directory to download to')
    parser.add_argument('--keep-zips', action='store_true', help='Keep zip files after extraction')

    args = parser.parse_args()

    try:
        main_download(args.keys, args.dir, args.keep_zips)
    except Exception as e:
        print(f"Failed to run with error: {str(e)}")