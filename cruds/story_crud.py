from typing import List

from bson import ObjectId

from cruds.page_crud import remove_page
from db import story_collection, story_meta_collection
from workers.page import save_page, save_last_page


def fetch_story(id: str):
    story = story_collection.find_one({'_id': ObjectId(id)})
    return {
        "id": str(story["_id"]),
        "title": story["title"],
        "cover_image_url": story["cover_image_url"],
        "page_count": story["page_count"],
        "created_date": story["created_date"],
        "pages_id_list": story["pages_id_list"]
    }


def fetch_all_stories():
    stories = story_collection.find()
    return [{
        "id": str(story["_id"]),
        "title": story["title"],
        "cover_image_url": story["cover_image_url"],
        "page_count": story["page_count"],
        "created_date": story["created_date"],
        "pages_id_list": story["pages_id_list"]
    } for story in stories]


def init_story(source: str):
    # TODO: gpt 문장 옵션 생성에 필요한 파라미터 -> source
    content_options = ["문장1"]  # GPT가 생성한 문장

    meta = story_meta_collection.insert_one({
        "page_content_options": content_options
    })

    inited_story = story_collection.insert_one({
        "source": source,
        "meta_id": str(meta.inserted_id)
    })

    return {
        "story_id": str(inited_story.inserted_id),
        "content_options": content_options
    }


def save_story_page(story_id: str, page_index: str, selected_content_option: str):
    # 마지막 페이지이면 표지 URL 반환
    if page_index is "10":
        return save_last_page(story_id, selected_content_option)

    return save_page(story_id, page_index)


def fetch_story_contents(story_id: str) -> List[str]:
    story = story_collection.find_one({'_id': ObjectId(story_id)})
    page_contents = story["page_contents"]

    return page_contents


def confirm_story_contents(story_id: str, confirm_contents: List[str]) -> str:
    story_collection.find_one_and_update(
        {'_id': ObjectId(story_id)},
        {"$set": {"page_contents": confirm_contents}}
    )

    return story_id


def finalize_save_story(story_id: str, title: str, cover_image_url: str):
    story_collection.update_one(
        {"_id": ObjectId(story_id)},
        {"$set": {
            "title": title,
            "cover_image_url": cover_image_url
        }}
    )

    return story_id


def remove_story(story_id: str) -> None:
    deleted_story = story_collection.find_one_and_delete({"_id": ObjectId(story_id)})
    meta_id = deleted_story["meta_id"]

    remove_story_meta(meta_id)


def remove_story_meta(meta_id: str):
    story_meta_collection.delete_one({"_id": ObjectId(meta_id)})