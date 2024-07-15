from typing import List

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import requests
import os
from aws import S3Manager

s3 = S3Manager()

_ = load_dotenv(find_dotenv())
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)


def generate_image(prompt: str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return response.data[0].url


def download_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content  # 이미지 데이터 반환
    else:
        raise Exception(f"Failed to download image from {url}. Status code: {response.status_code}")


def generate_images_from_contents(contents: List[str]):

    contents_images = []

    for content in contents:
        img_data = download_image_from_url(generate_image(content))
        img_url = s3.upload_image_on_s3(img_data)
        contents_images.append(img_url)

    return contents_images


# 이미지 여러 개 뽑는 법은?
def generate_cover_images(contents: List[str]):
    story = ', '.join(contents)

    img_data = download_image_from_url(generate_image(story))
    return s3.upload_image_on_s3(img_data)


sample_img = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-hSYk9Q432nurwoMVLYJDpPRz/user-2bXD6y0WDFF4E32FXWAK3UE7/img-Z49uCRWGbgslTzuWSRqMoeBq.png?st=2024-07-14T14%3A45%3A24Z&se=2024-07-14T16%3A45%3A24Z&sp=r&sv=2023-11-03&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-07-14T01%3A23%3A56Z&ske=2024-07-15T01%3A23%3A56Z&sks=b&skv=2023-11-03&sig=nM2fE7y74orfpiyNfuI5AIDMSThbyWbjoKOyC7jrYnw%3D"
# print(s3.upload_image_on_s3(download_image_from_url(sample_img)))