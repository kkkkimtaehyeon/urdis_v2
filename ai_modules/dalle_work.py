import asyncio
from datetime import time
from typing import List
from openai import AsyncOpenAI

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import requests
import os
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


def generate_cover_images(summary: str):
    urls = []

    for _ in range(0, 2):
        urls.append(generate_image(summary))

    img_datas = download_image_from_url(urls)

    return [s3.upload_image_on_s3(img_data) for img_data in img_datas]


async def test_generator(prompt: str):
    response = await async_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

    return response.data[0].url


story_lines = [
    "우리는 큰 나무 아래에 돗자리를 깔고, 맛있는 음식을 나눠 먹었어요. 엄마는 맛있는 김밥을 싸왔고, 할머니는 따뜻한 된장국을 준비했죠한번은 할머니께서 재미난 이야기를 들려주셨어요. 옛날 옛날에 작은 마을에 살던 아기 돼지 삼형제 이야기를 시작하셨어요",
    "놀이터 한쪽에서는 아빠와 동생이 비눗방울을 불며 놀고 있었어요. 비눗방울이 하늘로 날아가며 반짝반짝 빛났죠",
    "그때, 작은 새 한 마리가 놀이터 나무 위로 날아왔어요. 새는 노란색과 파란색이 섞인 깃털을 가지고 있었어요. \"와, 정말 예쁘다!\"라고 나는 외쳤어요. 모두가 작은 새를 바라보며 웃었어요",
    "작은 새는 우리 가족을 보고 조금 망설였지만, 곧 용기를 내어 나와 가까이 다가왔어요. 나와 새는 눈이 마주쳤고, 나는 살며시 손을 뻗어 새에게 인사했어요",
    "새는 내 손가락에 앉아 천천히 내 손을 올라갔어요. 나는 두근거리는 마음을 감출 수 없었어요. 작은 새의 부드러운 깃털이 내 손에 닿자, 기분 좋은 감촉이 느껴졌어요. 나와 새는 이렇게 서로를 바라보며 한참 동안 조용히 시간을 보냈어요",
    "그러던 중, 작은 새가 반짝이는 무언가를 떨어뜨렸어요. 나는 그것이 무엇인지 궁금해서 살펴보니, 작은 보석 같았어요. 우리 가족은 그 보석을 보고 경이로움을 느꼈어요",
    "보석을 손에 든 순간, 작은 새는 다시 날아올라 하늘로 사라졌어요. 하지만 보석을 통해 나는 뭔가 특별한 것을 느꼈어요. 가족들 모두 나에게 관심을 가지며 그 보석이 무엇인지 궁금해했어요",
    "나는 손에 든 보석을 자세히 들여다봤어요. 갑자기 그 안에서 빛이 뿜어져 나왔고, 우리 가족은 눈을 살짝 감았어요. 빛이 사라지자, 우리는 아름다운 꽃밭 한가운데에 서 있었어요. 가족들은 놀라움과 경이로움에 말을 잃었어요",
    "우리는 갑자기 나타난 꽃밭을 보고 놀라움에 빠졌어요. 나비들이 우리 주위를 날아다니며 춤을 추듯이 움직였어요. 아빠는 꽃 한 송이를 꺾어서 내게 주었고, 엄마는 그 향기를 맡으며 미소를 지었어요. 모두 그 순간을 행복하게 즐겼어요",
    "그 순간, 하늘에서 부드러운 음악이 들려왔어요. 우리 가족은 모두 손을 잡고 원을 만들며 춤을 추기 시작했어요. 나비들도 우리 주위를 맴돌며 춤을 춰주는 것 같았어요. 음악이 끝날 때쯤, 우리는 서로의 눈을 바라보며 환한 미소를 지었어요. 그 뒤로도 우리는 꽃밭에서 계속 놀며, 그 순간을 오래도록 기억하기로 했어요. 엄마와 아빠도 나에게 소중한 기억으로 오래 남을 거라고 했어요"
  ]


async def dalle_test():
    for line in story_lines:
        response = await test_generator(line)
        print(f"url: {response}")


# asyncio.run(dalle_test())
