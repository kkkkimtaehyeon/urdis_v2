from typing import List

from bson import ObjectId
from db import story_meta_collection, story_collection
from schemas import UserOptions


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
            "$set": {
                f"pages.contents.{current_page}": options.options,
                f"selected_option.{current_page}": options.selected_option_index
            }
        },
        upsert=True
    )


def sse_confirm_contents(story_id: str, contents_list: List[str]):
    story = story_collection.update_one(
        {"_id": ObjectId(story_id)},
        {"$set": {"contents": contents_list}},
        upsert=True
    )

    return str(story['_id'])