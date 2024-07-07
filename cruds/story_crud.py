from typing import Optional

from bson import ObjectId

from aws import upload_image_on_s3, delete_image_on_s3
from db import story_collection, story_meta_collection
from schemas import Story
from cruds.page_crud import remove_page


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


def save_story_page(story_id: str, selected_content_option: str, last_page: Optional[bool]):
    if last_page:
        story = story_collection.find_one_and_update(
            {"_id": ObjectId(story_id)},
            {"$push": {
                "page_contents": selected_content_option
            }})

        # TODO: 달리한테 이미지 생성 요청
        # TODO: 생성된 이미지 S3 업로드
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

    story = story_collection.find_one_and_update(
        {"_id": ObjectId(story_id)},
        {"$push": {
            "page_contents": selected_content_option
        }})

    selected_contents = story['page_contents']
    meta_id = story['meta_id']
    print(selected_contents)
    # TODO: gpt 문장 옵션 생성에 필요한 파라미터 -> selected_contents
    content_options = ["문장 옵션 1", "문장 옵션 2", "문장 옵션 3"]  # GPT가 생성한 문장

    story_meta_collection.update_one(
        {"_id": ObjectId(meta_id)},
        {"$push": {"page_content_options": content_options}},
    )

    return {
        "story_id": story_id,
        "content_options": content_options
    }


def finalize_save_story(story_id: str, title: str, cover_image_url: str):
    story_collection.update_one(
        {"_id": ObjectId(story_id)},
        {"$set": {
            "title": title,
            "cover_image_url": cover_image_url
        }}
    )

    return story_id


def save_story(title, cover_image, source, pages_id_list) -> str:
    cover_image_url = upload_image_on_s3(file=cover_image)
    story = Story(
        title=title,
        cover_image_url=cover_image_url,
        source=source,
        pages_id_list=pages_id_list[0].split(",")
    )
    saved_story = story_collection.insert_one(dict(story))

    return str(saved_story.inserted_id)


# TODO: source도 삭제
def remove_story(id: str) -> None:
    try:
        story = story_collection.find_one({'_id': ObjectId(id)})
        if story is None:
            print(f"Story with id {id} not found.")
            return

        pages_id_list = story["pages_id_list"]

        delete_image_on_s3(story["cover_image_url"])

        try:
            story_collection.delete_one({'_id': ObjectId(id)})
            # 페이지 삭제
            for page_id in pages_id_list:
                remove_page(page_id)
        except Exception as e:
            print(f"Failed to delete story from collection: {e}")
            return

    except Exception as e:
        print(f"Unexpected error: {e}")
