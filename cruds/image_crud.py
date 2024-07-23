from typing import List

from bson import ObjectId

from ai_modules.dalle_work import generate_cover_image, test_generator, get_data_from_url
from db import story_collection, story_meta_collection
from aws import S3Manager
from ai_modules.gpt_work import summarizer, generate_summary_prompt

s3 = S3Manager()


def show_content_with_images(story_id: str, page: int) -> tuple:
    story = story_collection.find_one({'_id': ObjectId(story_id)})
    story_meta = story_meta_collection.find_one({'_id': ObjectId(story['story_meta_id'])})

    return story['contents'][page - 1], story_meta['images'][page - 1]


def select_images(story_id: str, selected_images: List[str]):
    story = story_collection.find_one_and_update(
        {"_id": ObjectId(story_id)},
        {"$set": {"images": selected_images}})

    # print("요약중...")
    # summarized_prompt = generate_summary_prompt(story['contents'])
    # summary = summarizer(summarized_prompt)
    # print("요약 완료.")
    #
    # print("표지 생성중...")
    # cover_images = generate_cover_images(summary)
    # print("표지 생성 완료.")
    #
    # # 더미 데이터
    # cover_images = ["https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/one.png",
    #                 "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/two.png",
    #                 "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/three.png",
    #                 "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/four.png"]
    #
    # story_meta_id = story['story_meta_id']
    #
    # update_cover_images(story_meta_id, cover_images)


def update_cover_images(story_meta_id: str, cover_images: List[str]):
    story_meta_collection.update_one(
        {'_id': ObjectId(story_meta_id)},
        {'$set': {'cover_images': cover_images}},
        upsert=True
    )


def show_cover_images(story_id: str) -> List[str]:
    story = story_collection.find_one({'_id': ObjectId(story_id)})

    story_meta = story_meta_collection.find_one({'_id': ObjectId(story['story_meta_id'])})
    cover_images = story_meta['cover_images']

    return cover_images


def update_generated_image_in_background(story_id: str, content: str):
    # # 이미지 생성
    # image_url = test_generator(content)
    # # 이미지 데이터 추출
    # image_data = get_data_from_url(image_url)
    # # s3에 생성된 이미지 데이터 업로드
    # uploaded_url = s3.upload_image_on_s3(image_data)

    uploaded_url = "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/06172cb1-1367-4934-83fd-26f449f1d9d8"

    story = story_collection.find_one({'_id': ObjectId(story_id)})

    story_meta_collection.update_one(
        {'_id': ObjectId(story['story_meta_id'])},
        {"$push": {"images": uploaded_url}},
        upsert=True
    )


def update_cover_image_in_background(story_id: str, contents: List[str], n: int):

    prompt = generate_summary_prompt(contents)
    # 내용 요약
    summary = summarizer(prompt)

    # 요약된 내용으로 표지 생성
    uploaded_urls = ["https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/06172cb1-1367-4934-83fd-26f449f1d9d8", "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/06172cb1-1367-4934-83fd-26f449f1d9d8"]

    # for _ in range(n):
    #     cover_url = generate_cover_image(summary)
    #     # 이미지 데이터 추출
    #     image_data = get_data_from_url(cover_url)
    #     # s3에 생성된 이미지 데이터 업로드
    #     uploaded_urls.append(s3.upload_image_on_s3(image_data))

    story = story_collection.find_one({'_id': ObjectId(story_id)})

    story_meta_collection.update_one(
        {'_id': ObjectId(story['story_meta_id'])},
        {"$set": {"cover_images": uploaded_urls}},
        upsert=True
    )


