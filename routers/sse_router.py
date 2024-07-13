import asyncio
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from cruds.sse_crud import sse_init_story, sse_save_options_and_index, sse_confirm_contents
from routers.story_router import dummy_text2
from schemas import Source, UserOptions

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
    story_id = sse_confirm_contents(story_id, contents_list)

    return story_id


async def text_stream():
    for text in dummy_text2:
        yield f"data: {text}\n\n"
        await asyncio.sleep(0.5)