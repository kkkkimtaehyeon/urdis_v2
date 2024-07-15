import asyncio
from typing import List

from bson import ObjectId
from fastapi import APIRouter
from pydantic import BaseModel

from cruds.sse_crud import sse_init_story, sse_save_options_and_index, sse_confirm_contents, sse_select_image, \
    sse_show_images
from db import story_collection, story_meta_collection
from routers.story_router import dummy_text2
from schemas import Source, UserOptions, ImageSelector
from ai_modules.dalle_work import generate_cover_images

router = APIRouter(tags=["sse"])


@router.post("/api/sse/stories/init")  # 동화 첫 생성
async def initialize_stories(source: Source) -> str:
    source_prompt = source.prompt
    story_id = sse_init_story(source_prompt)

    return story_id


@router.post("/api/sse/stories/{story_id}/pages/{current_page}/contents")
async def post_selected_option_with_options(story_id: str, current_page: int, options: UserOptions):
    sse_save_options_and_index(story_id, current_page, options)


@router.get("/api/sse/stories/{story_id}/pages/{current_page}/contents")
async def get_options_with_sse(story_id: str, current_page: int):
    if current_page == 1:
        # return StreamingResponse(text_stream(), media_type="text/event-stream")
        return {
            "options": ["선택지 1"]
        }

    return {
        "options": ["선택지 1", "선택지 2", "선택지 3"]
    }


class ContentsConfirm(BaseModel):
    contents: List[str]


@router.post("/api/sse/stories/{story_id}/contents")
async def confirm_story_contents(story_id: str, contents_confirm: ContentsConfirm) -> str:
    contents_list = contents_confirm.contents
    sse_confirm_contents(story_id, contents_list)

    return story_id


async def text_stream():
    for text in dummy_text2:
        yield f"data: {text}\n\n"
        await asyncio.sleep(0.5)


@router.get("/api/sse/stories/{story_id}/pages/{page_index}/images")
async def show_images(story_id: str, page_index: int):
    content, images = sse_show_images(story_id, page_index)

    return {
        "content": content,
        "images": images
    }


class ImagesSelect(BaseModel):
    selected_images: List[str]


@router.post("/api/sse/stories/{story_id}/images")
async def selected_image(story_id: str, image_select: ImagesSelect):
    story = story_collection.find_one_and_update(
        {"_id": ObjectId(story_id)},
        {"$set": {"images": image_select.selected_images}})

    # 아직 이미지 하나만 뽑음, 여러 개 뽑게 수정 필요
    #cover_images = generate_cover_images(story['contents'])

    cover_images = ["https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/one.png",
                             "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/two.png",
                             "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/three.png",
                             "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/four.png"]

    story_meta_collection.update_one(
        {'_id': ObjectId(story['story_meta_id'])},
        {'$set': {'cover_images': cover_images}},
        upsert=True
    )

    return story_id
