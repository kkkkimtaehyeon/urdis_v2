from fastapi import APIRouter, BackgroundTasks
from starlette.responses import StreamingResponse

from ai_modules.gpt_work import test_generator
from cruds.image_crud import update_generated_image_in_background
from cruds.sse_crud import sse_init_story, sse_save_options_and_index, sse_confirm_contents
from cruds.story_crud import generate_gpt_messages
from schemas import Source, UserOptions, ContentsConfirm

router = APIRouter(tags=["sse"])


@router.post("/api/sse/stories/init")  # 동화 첫 생성
async def initialize_stories(source: Source) -> str:
    source_prompt = source.prompt
    story_id = sse_init_story(source_prompt)

    return story_id


@router.post("/api/sse/stories/{story_id}/pages/{current_page}/contents")
async def post_selected_option_with_options(story_id: str, current_page: int, options: UserOptions, background_tasks: BackgroundTasks):

    content_options = options.options
    index = options.selected_option_index

    print(f"내용: {content_options[index]}")

    sse_save_options_and_index(story_id, current_page, options)
    background_tasks.add_task(update_generated_image_in_background, story_id, content_options[index])

    return {"message": "background working"}


@router.get("/api/sse/stories/{story_id}/pages/{current_page}/contents")
async def get_options_with_sse(story_id: str, current_page: int):
    messages = generate_gpt_messages(story_id, current_page)

    return StreamingResponse(test_generator(messages), media_type="text/event-stream", headers={"Content-Encoding": "utf-8"})


@router.post("/api/sse/stories/{story_id}/contents")
async def confirm_story_contents(story_id: str, contents_confirm: ContentsConfirm) -> str:
    contents_list = contents_confirm.contents
    sse_confirm_contents(story_id, contents_list)

    return story_id