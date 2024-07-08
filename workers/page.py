from db import story_collection, story_meta_collection
from bson import ObjectId


def save_page(story_id: str, selected_content_option: str):
    story = story_collection.find_one_and_update(
        {"_id": ObjectId(story_id)},
        {"$push": {
            "page_contents": selected_content_option
        }})

    selected_contents = story['page_contents']  # gpt 문장 옵션 생성에 필요한 파라미터
    meta_id = story['meta_id']

    content_options = ["문장 옵션 1", "문장 옵션 2", "문장 옵션 3"]  # GPT가 생성한 문장

    story_meta_collection.update_one(
        {"_id": ObjectId(meta_id)},
        {"$push": {"page_content_options": content_options}},
    )

    return {
        "story_id": story_id,
        "content_options": content_options
    }


def save_last_page(story_id: str, selected_content_option: str):
    story = story_collection.find_one_and_update(
        {"_id": ObjectId(story_id)},
        {"$push": {
            "page_contents": selected_content_option
        }})

    # cover_image_url_options = generate_cover_from_story(story['page_contents'])
    cover_image_url_options = ["url1", "url2", "url3"]

    meta_id = story['meta_id']
    story_meta_collection.update_one(
        {"_id": ObjectId(meta_id)},
        {"$set": {"cover_image_url_options": cover_image_url_options}},
    )

    return {
        "story_id": story_id,
        "cover_image_url_options": cover_image_url_options
    }