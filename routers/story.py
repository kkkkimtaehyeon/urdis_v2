from typing import List

from fastapi import APIRouter, File, UploadFile, Form

from cruds.story_crud import fetch_story, fetch_all_stories, init_story, save_story, remove_story
from schemas import Story

router = APIRouter(tags=['story'])


@router.get("/api/stories/{id}")
async def get_stories(id: int) -> Story:
    return fetch_story(id)


@router.get("/api/stories")
async def get_stories() -> List[Story]:
    return fetch_all_stories()

@router.post("/api/stories/init")
async def initialize_story(source: str) -> str:
    return init_story(source)


@router.post("/api/stories/")
async def create_story(
        title: str = Form(...),
        cover_image: UploadFile = File(...),
        source: str = Form(...),
        pages_id_list: List[str] = Form(...)) -> str:
    return save_story(title, cover_image, source, pages_id_list)


@router.delete("/api/stories/{id}")
async def delete_story(id: str) -> None:
    remove_story(id)