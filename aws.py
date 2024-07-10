from fastapi import UploadFile, File
import boto3
import os
import uuid
from dotenv import load_dotenv, find_dotenv


def extract_object_key(url: str) -> str:
    return url.split("com/")[-1]


def generate_object_key(file) -> str:
    return str(uuid.uuid4()) + "_" + file.filename


class S3Manager:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
        self.AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
        self.BUCKET = os.getenv('AWS_S3_BUCKET')
        self.REGION = os.getenv('AWS_S3_REGION')
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.AWS_ACCESS_KEY,
            aws_secret_access_key=self.AWS_SECRET_KEY
        )

    def upload_on_s3(self, file: UploadFile = File()) -> str:
        key = generate_object_key(file)
        content_type = file.content_type
        self.s3.put_object(Body=file.file, Bucket=self.BUCKET, Key=key, ContentType=content_type)
        return f'https://{self.BUCKET}.s3.{self.REGION}.amazonaws.com/{key}'

    # aiobotocore, aioboto3로 대체 필요함
    def upload_image_on_s3(self, image_data: bytes) -> str:
        key = str(uuid.uuid4())
        content_type = "image/jpg"
        self.s3.put_object(Bucket=self.BUCKET, Body=image_data, Key=key, ContentType=content_type)
        return f'https://{self.BUCKET}.s3.{self.REGION}.amazonaws.com/{key}'

    def delete_image_on_s3(self, url: str):
        key = extract_object_key(url)
        try:
            self.s3.delete_object(Bucket=self.BUCKET, Key=key)
        except Exception as e:
            print(f"Failed to delete image on S3: {e}")
            return


