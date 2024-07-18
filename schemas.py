from typing import List

from pydantic import BaseModel


class Source(BaseModel):
    prompt: str


class StoryFinalizer(BaseModel):
    title: str
    author: str
    cover_image: str


class UserOptions(BaseModel):
    options: List[str]
    selected_option_index: int


class ImagesSelect(BaseModel):
    selected_images: List[str]


class ContentsConfirm(BaseModel):
    contents: List[str]