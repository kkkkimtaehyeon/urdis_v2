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
        model="dall-e-2",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=2,
    )

    return [image.url for image in response.data]


def download_image_from_url(urls: List[str]):
    image_datas = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            image_datas.append(response.content)  # 이미지 데이터 반환
        else:
            raise Exception(f"Failed to download image from {url}. Status code: {response.status_code}")

    return image_datas


def generate_images_from_contents(contents: List[str]):

    contents_images = []

    for content in contents:
        img_datas = download_image_from_url(generate_image(content))
        img_urls = [s3.upload_image_on_s3(img_data) for img_data in img_datas]
        contents_images.append(img_urls)

    return contents_images


def generate_cover_images(contents: List[str]):
    story = ', '.join(contents)
    img_datas = download_image_from_url(generate_image(story))

    return [s3.upload_image_on_s3(img_data) for img_data in img_datas]



response = client.images.generate(
        model="dall-e-3",
        prompt="오늘은 편의점에서 라면을 먹는 날이다. 지우는 아침부터 설레는 마음으로 일어났다. 오늘은 엄마와 함께 편의점에 가기로 한 날이기 때문이다. 지우는 엄마와 손을 잡고 집을 나섰다작은 마을에 사는 토끼 토미는 매주 금요일, 편의점에서 라면을 먹는 날을 손꼽아 기다렸어요. 안녕, 친구들이요! 오늘은 우리가 좋아하는 라면 날이에요",
        size="1024x1024",
        quality="standard",
        n=1,
    )

print(response)