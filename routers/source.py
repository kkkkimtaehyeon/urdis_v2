from fastapi import APIRouter, Depends
from cruds.source_crud import fetch_all_sources, fetch_source, save_source, remove_source
from schemas import Source

router = APIRouter(tags=['source'])


@router.get("/{id}")
async def get_source(id: str):
    return fetch_source(id)


@router.get("/")
async def get_all_sources():
    return fetch_all_sources()


@router.post("/")
async def create_source(source: Source):
    return save_source(source)


@router.delete("/{id}")
async def delete_source(id: str) -> None:
    remove_source(id)

