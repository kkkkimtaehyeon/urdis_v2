import json
import os
from typing import List

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CLIENT = OpenAI(api_key=OPENAI_API_KEY)


def generate_prompt(contents: List[str], page: int):
    history = " ,".join(contents)
    return [
        {"role": "system", "content": """너는 동화작가의 조수로, 동화작가를 도와서 발단, 전개, 절정, 결말을 가지는 구조의 글을 작성해.
    7살짜리 아이를 위한 동화를 작성하게 될거야. 총 10페이지의 동화를 작성하게 될거야."""},
        {"role": "user", "content": f'''지금까지의 이야기: ```{history}```

    너는 총 10문단 중 {page}번째 문단을 작성해야 하고, 총 3개의 다음 문단 후보를 작성해줘. 답변해줘야 할 format은 다음과 같아.
    
    {{'후보_1':"",
    '후보_2':"",
    '후보_3':""}}
         '''}
    ]


def generate_prompt_for_first(source: str):
    return [
        {"role": "system", "content": """너는 동화작가의 조수로, 동화작가를 도와서 발단, 전개, 절정, 결말을 가지는 구조의 글을 작성해.
    7살짜리 아이를 위한 동화를 작성하게 될거야. 총 10페이지의 동화를 작성하게 될거야."""},
        {"role": "user", "content": f'''지금까지의 이야기: ```{source}```

    너는 총 10문단 중 1번째 문단을 작성해야 하고, 총 1개의 다음 문단 후보를 작성해줘. 답변해줘야 할 format은 다음과 같아.
    {{'후보_1':"",
    }}
         '''}
    ]


async def test_generator(messages):
    output = ""
    response = CLIENT.chat.completions.create(
        # 모델 선언
        model="gpt-4o-2024-05-13",
        messages=messages,
        stream=True,
        # json 형태로 답변을 받기 위해 function call 형태 지정.
        functions=[
            {
                "name": "generate_fairytale",
                # 없어도 되긴 함
                "description": "Generate a fairytale in Korean with four parts: 후보_1, 후보_2, 후보_3",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "후보_1": {"type": "string", "description": "Introduction of the story"},
                        "후보_2": {"type": "string", "description": "Introduction of the story"},
                        "후보_3": {"type": "string", "description": "Introduction of the story"}
                    },
                    "required": ["후보_1", "후보_2", "후보_3"]
                }
            }
        ],
        function_call={"name": "generate_fairytale", "arguments": "{\"후보_1\": \"\",\"후보_2\": \"\",\"후보_3\": \"\"}"}
    )
    pre_length = 0
    for chunk in response:
        if chunk.choices[0].delta.function_call is not None and chunk.choices[
            0].delta.function_call.arguments is not None:

            output += chunk.choices[0].delta.function_call.arguments
            #print(output)

            try:
                output_change = output + '"}'
                output_change = json.loads(output_change)
            except:
                pass

            json_key_count = len(output_change)
            # gpt가 한번에 여러 문자 생성될 수도 있으니까 json value의 길이 비교해서 하기, -1 대신

            try:
                if json_key_count == 1:
                    full_length = len(output_change['후보_1'])
                    data = {"option1": str(output_change['후보_1'][pre_length:full_length])}
                    json_data = json.dumps(data)
                    #print(f"data: {json_data}\n\n")
                    yield f"data: {json_data}\n\n"
                    pre_length = full_length

            except:
                pass
            try:
                if json_key_count == 2:
                    full_length = len(output_change['후보_2'])
                    data = {"option2": str(output_change['후보_2'][pre_length:full_length])}
                    json_data = json.dumps(data)
                    #print(f"data: {json_data}\n\n")
                    yield f"data: {json_data}\n\n"
                    pre_length = full_length
            except:
                pass
            try:
                if json_key_count == 3:
                    full_length = len(output_change['후보_3'])
                    data = {"option3": str(output_change['후보_3'][pre_length:full_length])}
                    json_data = json.dumps(data)
                    #print(f"data: {json_data}\n\n")
                    yield f"data: {json_data}\n\n"
                    pre_length = full_length
            except:
                pass

    #print("data: [DONE]\n\n")
    yield "data: [DONE]\n\n"


def generate_summary_prompt(contents: List[str]):
    full_story = ",".join(contents)

    return [
        {"role": "system", "content": """너는 동화삽화 제작을 위해 한문장으로 내용을 요약해주는 AI야."""},
        {"role": "user", "content": f"동화 삽화 제작을 위해, 아래 문장을 한문장으로 요약해줘\n\n{full_story}"}]


def summarizer(messages):
    response = CLIENT.chat.completions.create(
        # 모델 선언
        model="gpt-4o-2024-05-13",
        messages=messages,
        stream=False,
        # json 형태로 답변을 받기 위해 function call 형태 지정.
        functions=[
            {
                "name": "generate_summarize",
                # 없어도 되긴 함
                "description": "Please summarize the contents in one sentence for the creation of fairy tale illustrations: 요약_결과",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "요약_결과": {"type": "string", "description": "Introduction of the story"},

                    },
                    "required": ["요약_결과"]
                }
            }
        ],
        function_call={"name": "generate_summarize", "arguments": "{\"요약_결과\": \"\"}"}
    )
    return json.loads(response.choices[0].message.function_call.arguments)['요약_결과']
