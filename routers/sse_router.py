from fastapi import APIRouter
from starlette.responses import StreamingResponse

from ai_modules.gpt_work import test_generator
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
async def post_selected_option_with_options(story_id: str, current_page: int, options: UserOptions):
    sse_save_options_and_index(story_id, current_page, options)


@router.get("/api/sse/stories/{story_id}/pages/{current_page}/contents")
async def get_options_with_sse(story_id: str, current_page: int):
    messages = generate_gpt_messages(story_id, current_page)

    return StreamingResponse(test_generator(messages), media_type="text/event-stream", headers={"Content-Encoding": "utf-8"})


@router.post("/api/sse/stories/{story_id}/contents")
async def confirm_story_contents(story_id: str, contents_confirm: ContentsConfirm) -> str:
    contents_list = contents_confirm.contents
    sse_confirm_contents(story_id, contents_list)

    return story_id

#
# @router.get("/api/sse/stories/{story_id}/pages/{page_index}/images")
# async def show_images(story_id: str, page_index: int):
#     content, images = sse_show_images(story_id, page_index)
#
#     return {
#         "content": content,
#         "images": images
#     }
#
#
# class ImagesSelect(BaseModel):
#     selected_images: List[str]
#
#
# @router.post("/api/sse/stories/{story_id}/images")
# async def selected_image(story_id: str, image_select: ImagesSelect):
#     story = story_collection.find_one_and_update(
#         {"_id": ObjectId(story_id)},
#         {"$set": {"images": image_select.selected_images}})
#
#     # 아직 이미지 하나만 뽑음, 여러 개 뽑게 수정 필요
#     #cover_images = generate_cover_images(story['contents'])
#
#     cover_images = ["https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/one.png",
#                              "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/two.png",
#                              "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/three.png",
#                              "https://urdis-bucket.s3.ap-northeast-2.amazonaws.com/four.png"]
#
#     story_meta_collection.update_one(
#         {'_id': ObjectId(story['story_meta_id'])},
#         {'$set': {'cover_images': cover_images}},
#         upsert=True
#     )
#
#     return story_id
