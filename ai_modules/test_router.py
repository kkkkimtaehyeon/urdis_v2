import asyncio
import json
import os
from typing import List

from dotenv import find_dotenv, load_dotenv
from fastapi import Request, APIRouter
from fastapi.responses import StreamingResponse
from openai import OpenAI

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CLIENT = OpenAI(api_key=OPENAI_API_KEY)
router = APIRouter()


def concat_contents(contents: List[str]):
    return ', '.join(contents)


def generate_prompt_for_contents_generator(prev_contents: List[str], current_page: int):
    history = concat_contents(prev_contents)
    n = current_page
    messages = [
        {"role": "system", "content": """너는 동화작가의 조수로, 동화작가를 도와서 발단, 전개, 절정, 결말을 가지는 구조의 글을 작성해.
    7살짜리 아이를 위한 동화를 작성하게 될거야. 총 10페이지의 동화를 작성하게 될거야."""},
        {"role": "user", "content": f'''지금까지의 이야기: ```{history}```
    너는 총 10문단 중 {n}번째 문단을 작성해야 하고, 총 3개의 다음 문단 후보를 작성해줘. 문단후보는 /로 구분해서 출력해줘
         '''}
    ]

    return messages


@router.post("/generate_content")
async def generate_content(request: Request):
    body = await request.json()
    prev_contents = body.get("prev_contents", [])
    current_page = body.get("current_page", 1)

    async def event_generator():
        messages = generate_prompt_for_contents_generator(prev_contents, current_page)
        # response = CLIENT.chat.completions.create(
        #     # 모델 선언
        #     model="gpt-3.5-turbo",
        #     messages=messages,
        #     stream=True,
        # )

        # for chunk in response:
        #     char = chunk.choices[0].delta.content
        #     if char == "/":
        #         yield "data: <<<OPTION_END>>>\n\n"
        #     yield f"data: {char}\n\n"
        #
        # yield "data: [DONE]\n\n"
        for char in dummy_data:
            if char == "/":
                yield "data: <<<OPTION_END>>>\n\n"
            yield f"data: {char}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream", headers={"Content-Encoding": "utf-8"})


dummy_data = """
이상한 할머니는 손에 큰 바구니를 들고 있었는데, 그 바구니 안에는 빨간 사과들이 가득했어. 할머니가 나를 보자 미소 짓더니 "안녕, 꼬마야. 내 손 아래로 빨간 사과 좀 올려줄래?" 라고 말했어./
나는 이상한 할머니에게 공손하게 인사를 하고, 소세지를 든 장바구니를 보여주며 "할머니, 오늘은 마트에 가서 소세지를 샀어요. 소세지 좋아하세요?" 라고 물어봤어./
할머니는 내 말에 미소 지으며 "소세지야? 나도 소세지가 너무 좋아. 빨간 사과 대신 소세지로 교환해볼까?" 라고 말하더니, 소세지와 사과를 하나씩 바구니에 넣기 시작했어.
"""


# async def generate_content(request: Request):
#     async def event_generator():
#         candidates = ["후보_1", "후보_2", "후보_3"]
#         for candidate in candidates:
#             for char in f"{candidate}의 내용입니다...":
#                 yield f"data: {char}\n\n"
#                 await asyncio.sleep(0.1)  # 실제 생성 속도를 시뮬레이션
#             yield "data: <<<OPTION_END>>>\n\n"  # 옵션 구분자
#         yield "data: [DONE]\n\n"
#
#     return StreamingResponse(event_generator(), media_type="text/event-stream")