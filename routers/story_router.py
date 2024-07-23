from typing import Dict, Any, List, Optional

from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter

from cruds.story_crud import fetch_all_stories, fetch_story, finalize_story, fetch_page
from schemas import StoryFinalizer

_ = load_dotenv(find_dotenv())
router = APIRouter(tags=["story"])


@router.get("/api/stories")  # 전체 동화 조회
async def get_all_stories(keyword: Optional[str] = None) -> List[Dict[str, Any]]:
    stories = fetch_all_stories(keyword)

    return [{
        "id": str(story["_id"]),
        "title": story["title"],
        "author": story["author"],
        "cover_image_url": story["cover_image"],
        "created_date": story['created_date']
    } for story in stories]


@router.get("/api/stories/{story_id}")
async def get_one_story(story_id) -> Dict:
    story = fetch_story(story_id)

    return {
        "id": str(story['_id']),
        "title": story['title'],
        "author": story['author'],
        "cover_image": story['cover_image'],
        "contents": story['contents'],
        "images": story['images'],
        "voices": story['contents_voices'],
        "created_date": story['created_date']
    }


@router.post("/api/stories/{story_id}/final")
async def post_title_author_cover(story_id: str, story_finalizer: StoryFinalizer) -> str:
    finalize_story(story_id, story_finalizer.title, story_finalizer.author, story_finalizer.cover_image)

    return story_id


@router.get("/api/stories/{story_id}/pages/{page_index}")
async def read_page(story_id: str, page_index: int):
    content, image = fetch_page(story_id, page_index)

    return {
        "contents": content,
        "image": image
    }

