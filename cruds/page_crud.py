from typing import Optional, Annotated

from bson import ObjectId
from fastapi import UploadFile, File, Form

from aws import upload_image_on_s3, delete_image_on_s3
from db import page_collection
from schemas import Page
from typing import List


def fetch_page(id: str):
    page = page_collection.find_one({'_id': ObjectId(id)})
    return {
        "content": page['content'],
        "image_url": page['image_url']
    }


def save_page_content(content_options: List[str]):
    pass

def save_page(content: str, image_file: UploadFile = File()):
    image_url = upload_image_on_s3(image_file)
    page = Page(content=content, image_url=image_url)
    saved_page = page_collection.insert_one(dict(page))
    return str(saved_page.inserted_id)


def edit_page(
        id: str, content: Annotated[Optional[str], Form()], image_file: Annotated[Optional[UploadFile], File()]):
    if content is not None:
        edit_page_content(id, content)
    if image_file is not None:
        edit_page_image_url(id, image_file)
    return id


def edit_page_content(id: str, content: str) -> None:
    page = page_collection.find_one_and_update({'_id': ObjectId(id)}, {'$set': {'content': content}})


def edit_page_image_url(id: str, image_file: UploadFile = File()) -> None:
    # 기존 이미지 존재하면 삭제
    page = page_collection.find_one({'_id': ObjectId(id)})
    if page['image_url'] is not None:
        delete_image_on_s3(page['image_url'])

    # 업데이트할 이미지 업로드
    updated_image_url = upload_image_on_s3(image_file)
    page_collection.update_one({'_id': ObjectId(id)}, {'$set': {'content': updated_image_url}})


def remove_page(id: str) -> None:
    try:
        page = page_collection.find_one({'_id': ObjectId(id)})

        if page is None:
            print(f"Story with id {id} not found.")
            return

        image_url = page['image_url']

        delete_image_on_s3(url=image_url)

        try:
            page_collection.delete_one({'_id': ObjectId(id)})
        except Exception as e:
            print(f"Failed to delete page from collection: {e}")
            return

    except Exception as e:
        print(f"Unexpected error: {e}")


def generate_page_content_options(source: str, pages_id_list: List[str], first: bool):
    if first:
        # TODO: GPT에서 문장 1개 생성 후 리턴
        gpt_response = ["문장 1"]
        return
    # TODO: GPT에서 문장 3개 생성 후 리턴
    return ["문장 1", "문장 2", "문장 3"]



