from typing import Dict, Any, List, Optional

from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter

from cruds.story_crud import fetch_all_stories, fetch_story, init_story, show_content_options, select_content_option, \
    fetch_story_contents, confirm_contents, finalize_story, fetch_page
from schemas import Source, OptionSelector, StoryFinalizer

_ = load_dotenv(find_dotenv())
router = APIRouter(tags=["story"])
dummy_text2 = "안녕하세요! 저는 인공지능 언어모델인 GPT-3입니다."


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
        "created_date": story['created_date']
    }


# @router.post("/api/stories/init")  # 동화 첫 생성
# async def initialize_stories(source: Source) -> str:
#     source_prompt = source.prompt
#     story_id = init_story(source_prompt)
#
#     return story_id


@router.post("/api/stories/{story_id}/final")
async def post_title_author_cover(story_id: str, story_finalizer: StoryFinalizer) -> str:
    finalize_story(story_id, story_finalizer.title, story_finalizer.author, story_finalizer.cover_image)

    return story_id


# @router.get("/api/stories/{story_id}/contents/{content_index}")
# async def get_content_options(story_id: str, content_index: int) -> Dict:
#     options = show_content_options(story_id, content_index)
#
#     return {
#         "options": options
#     }
#
#
# @router.post("/api/stories/{story_id}/contents/{content_index}")
# async def choose_content_option(story_id: str, content_index: int, option_selector: OptionSelector) -> str:
#     story_id = select_content_option(
#         story_id, content_index, option_selector.selected_option_content, option_selector.selected_option_index)
#
#     return story_id


# @router.get("/api/stories/{story_id}/contents")
# async def get_story_contents(story_id: str) -> Dict:
#     story_contents = fetch_story_contents(story_id)
#
#     return {
#         "contents": story_contents
#     }
#
#
# @router.post("/api/stories/{story_id}/contents")
# async def confirm_story_contents(story_id: str) -> str:
#     story_id = confirm_contents(story_id)
#
#     return story_id


@router.get("/api/stories/{story_id}/pages/{page_index}")
async def read_page(story_id: str, page_index: int):
    content, image = fetch_page(story_id, page_index)

    return {
        "contents": content,
        "image": image
    }





# @router.get("/api/stories/init/sse")
# async def testing_sse():
#     return StreamingResponse(time_stream(), media_type="text/event-stream")
#
#
# async def time_stream():
#     for _ in range(0,5):
#         current_time = time.strftime("%Y-%m-%d %H:%M:%S").encode('utf-8')
#         yield f"data: {current_time}\n\n"
#         await asyncio.sleep(0.1)
#
#
# @router.get("/api/stories/{story_id}/pages/{page_index}/sse")
# async def generate_text(story_id: str, page_index: int):
#     return StreamingResponse(text_stream(), media_type="text/event-stream")
#
#
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



