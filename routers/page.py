from fastapi import APIRouter, Depends, UploadFile, File, Form
from cruds.page_crud import fetch_page, save_page, edit_page, remove_page
from schemas import Page
from typing import Optional, Annotated

router = APIRouter(tags=['page'])


@router.get("/{id}")
async def get_page(id: str) -> Page:
    return fetch_page(id)


# 프론트에서 내용 리스트 저장하고 있다가 삽화 선택 시 저장
@router.post("")
async def create_page(content: str, image_file: UploadFile = File()):
    return save_page(content, image_file)


@router.patch("/{id}")
async def update_page(
        id: str,
        content: Optional[str] = Form(None),
        image_file: Optional[UploadFile] = File(None)):
    # TODO 쿼리 스트링으로 내용, 삽화 구분하거나 메서드 하나에서 if문으로 구분
    edited_page_id = edit_page(id, content, image_file)
    return edited_page_id


@router.delete("/{id}")
async def delete_page(id: str) -> None:
    remove_page(id)