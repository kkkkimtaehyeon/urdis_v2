from typing import List

from pydantic import BaseModel


class Source(BaseModel):
    prompt: str


class OptionSelector(BaseModel):
    selected_option_content: str
    selected_option_index: int


class ContentsReviewer(BaseModel):
    contents: List[str]


class StoryFinalizer(BaseModel):
    title: str
    author: str
    cover_image: str


class ImageSelector(BaseModel):
    selected_options_index: List[int]


class StoryResponse(BaseModel):
    story_id: str
    title: str
    author: str
    cover_image: str
    contents: List[str]
    images: List[str]
