import os
from typing import List
import json

from dotenv import find_dotenv, load_dotenv
from fastapi import Request
from fastapi.responses import JSONResponse
from openai import OpenAI

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CLIENT = OpenAI(api_key=OPENAI_API_KEY)


def concat_contents(contents: List[str]):
    return ', '.join(contents)


def generate_prompt_for_contents_generator(prev_contents: List[str], current_page: int):
    history = concat_contents(prev_contents)
    n = current_page
    messages = [
        {"role": "system", "content": """너는 동화작가의 조수로, 동화작가를 도와서 발단, 전개, 절정, 결말을 가지는 구조의 글을 작성해.
        7살짜리 아이를 위한 동화를 작성하게 될거야. 총 10페이지의 동화를 작성하게 될거야."""},
        {"role": "user", "content": f'''지금까지의 이야기: ```{history}```
        너는 총 10문단 중 {n}번째 문단을 작성해야 하고, 총 3개의 다음 문단 후보를 작성해줘. 각 문단후보의 마지막은 /로 구분해서 출력해줘
             '''}
    ]

    return messages


def generate_content_options(messages):

    response = CLIENT.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=messages,
        stream=True
    )

    for chunk in response:
        char = chunk.choices[0].delta.content
        if char == "/":
            yield "data: <<<OPTION_END>>>\n\n"
        yield f"data: {char}\n\n"
    yield "data: [DONE]\n\n"



prev_contents = ["오늘은 마트에 갔다", "마트에서 소세지를 샀다."]

prompt = generate_prompt_for_contents_generator(prev_contents, 3)

generate_content_options(prompt)
# contents_options = generate_content_options(prompt)
#
# print(contents_options)
