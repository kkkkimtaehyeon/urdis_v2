from typing import Dict

from fastapi import APIRouter

from cruds.image_crud import show_content_with_images, select_images, show_cover_images
from schemas import ImageSelector

router = APIRouter(tags=["image"])


# @router.get("/api/stories/{story_id}/pages/{page_index}/images")
# async def get_content_with_images(story_id: str, page_index: int) -> Dict:
#     content, images = show_content_with_images(story_id, page_index)
#
#     # return content_and_images
#     return {
#             "content": content,
#             "images": images
#         }


# @router.post("/api/stories/{story_id}/images")
# async def choose_images(story_id: str, image_selector: ImageSelector) -> str:
#     select_images(story_id, image_selector.selected_options_index)
#
#     return story_id


@router.get("/api/stories/{story_id}/covers")
async def get_cover_image_options(story_id: str):
    cover_image_options = show_cover_images(story_id)

    return {
        "options": cover_image_options
    }
