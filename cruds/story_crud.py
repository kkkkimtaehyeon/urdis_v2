from typing import List, Dict
import datetime
from bson import ObjectId

from db import story_collection, story_meta_collection


def fetch_all_stories() -> List[Dict]:
    stories = story_collection.find()
    return stories


# TODO
def fetch_story(story_id: str) -> Dict:
    story = story_collection.find_one({"_id": ObjectId(story_id)})

    return story


def init_story(source_prompt: str):
    # TODO: gpt가 source_prompt를 파라미터로 문장 하나를 생성하고 반환
    gpt_response = ["문장1"]
    story_meta = story_meta_collection.insert_one(
        {
            "source": source_prompt,
            "contents": gpt_response
        })

    story = story_collection.insert_one({"story_meta_id": str(story_meta.inserted_id)})

    story_id = str(story.inserted_id)

    return story_id


def finalize_story(story_id: str, title: str, author: str, cover_image: str):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    story_collection.update_one(
        {'_id': ObjectId(story_id)},
        {'$set': {'title': title, 'author': author, 'cover_image': cover_image, 'created_date': now_time}},
    )


def show_content_options(story_id: str, content_index: int) -> List[str]:
    story = story_collection.find_one({"_id": ObjectId(story_id)})
    story_meta = story_meta_collection.find_one({"_id": ObjectId(story['story_meta_id'])})

    return story_meta['contents'][content_index - 1]


def select_content_option(story_id: str, content_index: int, selected_option_content: str, selected_option_index: int):
    story = story_collection.find_one_and_update(
        {"_id": ObjectId(story_id)},
        {"$push": {"contents": selected_option_content}},
    )

    if content_index < 10:
        # TODO: gpt가 source_prompt를 파라미터로 문장 3개를 생성하고 반환
        gpt_response = ["문장1", "문장2", "문장3"]

        story_meta_collection.update_one(
            {"_id": ObjectId(story['story_meta_id'])},
            {"$push": {"contents": gpt_response}},
            upsert=True
        )

    return story_id


def fetch_story_contents(story_id: str) -> List[str]:
    story = story_collection.find_one({"_id": ObjectId(story_id)})

    return story['contents']


def confirm_contents(story_id: str, contents: List[str]):
    story = story_collection.find_one_and_update(
        {"_id": ObjectId(story_id)},
        {"$set": {"contents": contents}}
    )

    # TODO: 스토리 기반으로 10페이지 * 4개의 이미지 생성 -> s3 업로드 -> 이미지 URL 스토리 메타데이터에 저장
    # 이미지 저장할 때 같은 페이지에서 생성되는 이미지는 상관 없지만 페이지의 순서는 보장되어야 함
    uploaded_image_urls = [["url1", "url2", "url3", "url4"] for index in range(0, 10)]

    story_meta_collection.find_one_and_update(
        {"_id": ObjectId(story['story_meta_id'])},
        {"$set": {"images": uploaded_image_urls}}
    )

    return story_id
