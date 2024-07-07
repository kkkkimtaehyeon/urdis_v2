from typing import List

from fastapi import APIRouter

from fastapi import APIRouter

from cruds.story_crud import init_story, save_story_page, fetch_story_contents, finalize_save_story, confirm_story_contents, remove_story

router = APIRouter(tags=['story'])


# @router.get("/api/stories/{id}")
# async def get_stories(id: int) -> Dict:
#     return fetch_story(id)
#
#
# @router.get("/api/stories")
# async def get_stories() -> List[Dict]:
#     return fetch_all_stories()


@router.post("/api/stories/init")
async def initialize_story(source: str):
    return init_story(source)


@router.post("/api/stories{story_id}/pages/{page_index}")
async def create_story_page(story_id: str, page_index, selected_content_option: str):
    return save_story_page(story_id, page_index, selected_content_option)


@router.get("/api/stories{story_id}/contents/confirm")
async def get_contents(story_id: str) -> List[str]:
    return fetch_story_contents(story_id)


@router.post("/api/stories{story_id}/contents/confirm")
async def check_contents(story_id: str, contents: List[str]) -> str:
    return confirm_story_contents(story_id, contents)


@router.post("/api/stories/{story_id}/finalize")
async def finalize_story(story_id: str, title: str, cover_image_url: str):
    return finalize_save_story(story_id, title, cover_image_url)


@router.delete("/api/stories/{id}")
async def delete_story(story_id: str) -> None:
    remove_story(story_id)