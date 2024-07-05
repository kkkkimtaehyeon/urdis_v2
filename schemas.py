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

