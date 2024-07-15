from typing import List

from bson import ObjectId
from db import story_meta_collection, story_collection
from schemas import UserOptions, ImageSelect, ImageSelector
from ai_modules.dalle_work import generate_images_from_contents


def sse_init_story(source_prompt: str):
    story_meta = story_meta_collection.insert_one({"source": source_prompt})
    story = story_collection.insert_one({"story_meta_id": str(story_meta.inserted_id)})

    story_id = str(story.inserted_id)

    return story_id


def sse_save_options_and_index(story_id: str, current_page: int, options: UserOptions):
    story = story_collection.find_one({"_id": ObjectId(story_id)})
    story_meta_collection.update_one(
        {"_id": ObjectId(story['story_meta_id'])},
        {
            "$push": {
                "contents": options.options,
                "selected_content_option": options.selected_option_index
            }
        },
        upsert=True
    )


def sse_confirm_contents(story_id: str, contents_list: List[str]):
    story = story_collection.find_one_and_update(
        {"_id": ObjectId(story_id)},
        {"$set": {"contents": contents_list}},
        upsert=True
    )
    # 아직 페이지 하나 당 하나의 이미지만 생성
    # images = generate_images_from_contents(story['contents'])

    images = [["https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/one.png", "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/two.png", "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/three.png", "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/four.png"] for index in range(0, 10)]

    story_meta_collection.update_one(
        {"_id": ObjectId(story['story_meta_id'])},
        {"$set": {"images": images}}
    )


def sse_show_images(story_id: str, page_index: int):
    story = story_collection.find_one({"_id": ObjectId(story_id)})

    story_meta = story_meta_collection.find_one({"_id": ObjectId(story['story_meta_id'])})

    return story['contents'][page_index - 1], story_meta['images'][page_index - 1]


def sse_select_image(story_id: str, image_select: ImageSelector):
    story = story_collection.find_one({"_id": ObjectId(story_id)})

    story_meta_collection.update_one(
        {"_id": ObjectId(story['story_meta_id'])},
        {"$set": {"image_options": image_select.selected_options_index}}
    )

    #
    # dalle_response = "base64_format_response"
    # image_data = convert_base64_to_image(dalle_response)
    # s3.upload_image_on_s3(image_data)

    uploaded_cover_images = ["https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/one.png", "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/two.png", "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/three.png", "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/four.png"]

    story_meta_collection.update_one(
        {'_id': ObjectId(story['story_meta_id'])},
        {'$set': {'cover_images': uploaded_cover_images}},
        upsert=True
    )


