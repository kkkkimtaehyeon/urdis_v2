from typing import List

from fastapi import APIRouter
from ai_modules.image_generator import generate_cover_from_contents

router = APIRouter(tags=['illustration'])


@router.post("/api/illustrations")
async def create_illustration(type: str):
    if type is "contents":
        # 내용 이미지 생성하는 함수 추가
        pass

    else:  # cover
    # 표지 이미지 생성하는 함수 추가
        pass
