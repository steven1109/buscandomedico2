import logging
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ACCESS_KEY = 'AKIA5YXDO6KESBU2HM7A'
SECRET_ACCESS_KEY = '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'
dir = '/home/steven.jefferson.ve/Pictures'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_ACCESS_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_ACCESS_KEY)
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents


def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_ACCESS_KEY)
    output = f"/home/steven.jefferson.ve/Downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output


def show_image(bucket):
    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_ACCESS_KEY)
    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url(
                'get_object', Params={'Bucket': bucket, 'Key': item['Key']}, ExpiresIn=100)
            public_urls.append(presigned_url)
    except Exception as e:
        print(e)
        pass
    # print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls
