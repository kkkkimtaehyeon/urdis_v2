from datetime import datetime
from typing import List

from fastapi import UploadFile, File, Form
from pydantic import BaseModel, Field


class Source(BaseModel):
    prompt: str


class Story(BaseModel):
    title: str
    cover_image_url: str
    page_count: int = Field(default=12)
    created_date: str = Field(default=datetime.today().strftime('%Y/%m/%d %H:%M'))
    source: str
    pages_id_list: List[str]


# 프론트에서 페이지 아이디 리스트를 저장
class Page(BaseModel):
    content: str
    image_url: str


class PageMetadata(BaseModel):
    content_options: List[str]
    selected_content_index: int
    selected_content: str
    image_url_options: List[str] = Field(default=None)
    selected_image_url_index: int = Field(default=None)
    selected_image_url: str = Field(default=None)


class PageContentSaveRequest(BaseModel):
    content_options: List[str]
    selected_content_index: int
    selected_content: str


class PageImageSaveRequest(BaseModel):
    image_url_options: List[str]
    selected_image_url_index: int
    selected_image_url: str
