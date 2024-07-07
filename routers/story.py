from typing import List, Dict, Optional

from fastapi import APIRouter, File, UploadFile, Form

from cruds.story_crud import fetch_story, fetch_all_stories, init_story, save_story, remove_story, save_story_page, finalize_save_story
from schemas import Story

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
async def create_story_page(story_id: str, selected_content_option: str, last_page: Optional[bool] = None):
    return save_story_page(story_id, selected_content_option, last_page)


@router.post("/api/stories/{story_id}/finalize")
async def finalize_story(story_id: str, title: str, cover_image_url: str):
    return finalize_save_story(story_id, title, cover_image_url)


# @router.post("/api/stories/")
# async def create_story(
#         title: str = Form(...),
#         cover_image: UploadFile = File(...),
#         source: str = Form(...),
#         pages_id_list: List[str] = Form(...)) -> str:
#     return save_story(title, cover_image, source, pages_id_list)
#
#
# @router.delete("/api/stories/{id}")
# async def delete_story(id: str) -> None:
#     remove_story(id)