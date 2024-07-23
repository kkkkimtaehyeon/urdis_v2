import os
from typing import List

import requests
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from openai import OpenAI

from aws import S3Manager

s3 = S3Manager()

_ = load_dotenv(find_dotenv())
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
async_client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def generate_image(prompt: str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return response.data[0].url


def generate_cover_image(summary: str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"다음 내용에 맞는 동화의 표지를 그려줘: {summary}",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return response.data[0].url



# def download_image_from_url(urls: List[str]):
#     image_datas = []
#     for url in urls:
#         response = requests.get(url)
#         if response.status_code == 200:
#             image_datas.append(response.content)  # 이미지 데이터 반환
#         else:
#             raise Exception(f"Failed to download image from {url}. Status code: {response.status_code}")
#
#     return image_datas


# 이미지 url에서 이미지 데이터 추출
def get_data_from_url(url: str):
    response = requests.get(url)

    if response.status_code == 200:
        image_data = response.content  # 이미지 데이터 반환
    else:
        raise Exception(f"Failed to download image from {url}. Status code: {response.status_code}")

    return image_data


# def generate_images_from_contents(contents: List[str]):
#
#     contents_images = []
#
#     for content in contents:
#         img_datas = download_image_from_url(generate_image(content))
#         img_urls = [s3.upload_image_on_s3(img_data) for img_data in img_datas]
#         contents_images.append(img_urls)
#
#     return contents_images


def test_generator(prompt: str):
    response = client.images.generate(
            model="dall-e-3",
            prompt=f"다음 내용을 동화책의 삽화 느낌으로 글씨없이 오직 그림만 그려줘: {prompt}",
            size="1024x1024",
            quality="standard",
            n=1
        )
    print(response.data[0].url)
    return response.data[0].url