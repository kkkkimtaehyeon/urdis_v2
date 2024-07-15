from fastapi import APIRouter

from cruds.image_crud import select_images, show_cover_images
from cruds.sse_crud import sse_show_images
from schemas import ImagesSelect

router = APIRouter(tags=["image"])


@router.get("/api/sse/stories/{story_id}/pages/{page_index}/images")
async def show_images(story_id: str, page_index: int):
    content, images = sse_show_images(story_id, page_index)

    return {
        "content": content,
        "images": images
    }


@router.post("/api/sse/stories/{story_id}/images")
async def selected_image(story_id: str, image_select: ImagesSelect):
    select_images(story_id, image_select.selected_images)

    return story_id


@router.get("/api/stories/{story_id}/covers")
async def get_cover_image_options(story_id: str):
    cover_image_options = show_cover_images(story_id)

    return {
        "options": cover_image_options
    }
