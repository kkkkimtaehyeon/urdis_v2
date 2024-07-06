from bson import ObjectId

from aws import upload_image_on_s3, delete_image_on_s3
from db import story_collection
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
    # 빈 스토리 id를 각 페이지에 저장?
    inited_story = story_collection.insert_one({"source": source})
    return str(inited_story.inserted_id)


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
