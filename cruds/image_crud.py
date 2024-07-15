from typing import List

from bson import ObjectId

from db import story_collection, story_meta_collection
from aws import S3Manager


s3 = S3Manager()


def show_content_with_images(story_id: str, page: int) -> tuple:
    story = story_collection.find_one({'_id': ObjectId(story_id)})
    story_meta = story_meta_collection.find_one({'_id': ObjectId(story['story_meta_id'])})

    return story['contents'][page - 1], story_meta['images'][page - 1]


def select_images(story_id: str, selected_images: List[str]):
    story = story_collection.find_one_and_update(
        {"_id": ObjectId(story_id)},
        {"$set": {"images": selected_images}})

    # 아직 이미지 하나만 뽑음, 여러 개 뽑게 수정 필요
    # cover_images = generate_cover_images(story['contents'])

    cover_images = ["https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/one.png",
                    "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/two.png",
                    "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/three.png",
                    "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/four.png"]

    story_meta_collection.update_one(
        {'_id': ObjectId(story['story_meta_id'])},
        {'$set': {'cover_images': cover_images}},
        upsert=True
    )


def show_cover_images(story_id: str) -> List[str]:
    story = story_collection.find_one({'_id': ObjectId(story_id)})

    story_meta = story_meta_collection.find_one({'_id': ObjectId(story['story_meta_id'])})
    cover_images = story_meta['cover_images']

    return cover_images

