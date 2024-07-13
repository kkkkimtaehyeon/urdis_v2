from typing import List

from bson import ObjectId

from db import story_collection, story_meta_collection
from aws import S3Manager


s3 = S3Manager()


def show_content_with_images(story_id: str, page: int) -> tuple:
    story = story_collection.find_one({'_id': ObjectId(story_id)})
    story_meta = story_meta_collection.find_one({'_id': ObjectId(story['story_meta_id'])})

    return story['contents'][page - 1], story_meta['images'][page - 1]


def select_images(story_id: str, selected_options_index: List[int]):
    story = story_collection.find_one({'_id': ObjectId(story_id)})

    story_meta = story_meta_collection.find_one({'_id': ObjectId(story['story_meta_id'])})
    images_list = story_meta['images']
    selected_images = [images_list[i][selected_options_index[i]] for i in range(10)]

    story_collection.update_one(
        {'_id': ObjectId(story_id)},
        {'$set': {'images': selected_images}},
        upsert=True
    )

    # TODO: 표지 이미지 생성 -> s3 업로드
    # dalle_response = "base64_format_response"
    # image_data = convert_base64_to_image(dalle_response)
    # s3.upload_image_on_s3(image_data)

    uploaded_cover_images = ["cover_url1", "cover_url2", "cover_url3", "cover_url4"]

    story_meta_collection.update_one(
        {'_id': ObjectId(story['story_meta_id'])},
        {'$set': {'cover_images': uploaded_cover_images}},
        upsert=True
    )


def show_cover_images(story_id: str) -> List[str]:
    story = story_collection.find_one({'_id': ObjectId(story_id)})

    story_meta = story_meta_collection.find_one({'_id': ObjectId(story['story_meta_id'])})
    cover_images = story_meta['cover_images']

    return cover_images

