from fastapi import UploadFile, File
import boto3
import os
import uuid
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET = os.getenv('AWS_S3_BUCKET')
REGION = os.getenv('AWS_S3_REGION')

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)


def upload_image_on_s3(file: UploadFile = File()):
    key = generate_object_key(file)
    content_type = file.content_type
    s3.put_object(Body=file.file, Bucket=BUCKET, Key=key, ContentType=content_type)
    return f'https://{BUCKET}.s3.{REGION}.amazonaws.com/{key}'


def generate_object_key(file):
    return str(uuid.uuid4()) + "_" + file.filename


def delete_image_on_s3(url: str):
    # TODO s3에서 이미지 삭제
    key = extract_object_key(url)
    s3.delete_object(Bucket=BUCKET, Key=key)


def extract_object_key(url: str):
    return url.split("com/")[-1]