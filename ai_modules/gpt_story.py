import sys

from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
import os
_ = load_dotenv(find_dotenv())

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# prompt는 task에 따라 적절히 수정
messages = [
    {"role": "system", "content": "너는 동화작가의 조수로, 동화작가를 도와서 발단, 전개, 절정, 결말을 가지는 구조의 글을 작성해."},
    {"role": "user", "content": """7살짜리 아이를 위한 동화를 만들어줘. 개와 고양이가 등장하고, 친구들과 친하게 지내야 한다는 교훈을 담아야 해. 발단, 전개, 절정, 결말을 가지는 구조로 작성해줘.
     json fomat을 지켜서 답변해줘. json format은 아래와 같아.
     {'발단':""
     '전개':"",
     '절정':"",
     '결말':""}

     먼저 발단 부분을 작성해줘
     """}
]


# stream. 아마 서비스때는 async def 써야할 것
def stream(messages):
    # 진행되고 있는 대화를 저장해줄 때 쓰기 위해, 입력받은 메시지를 미리 저장해둠
    input_messages = messages.copy()

    response = client.chat.completions.create(
        # 모델 선언
        model="gpt-4o-2024-05-13",
        messages=messages,
        stream=True,
        # json 형태로 답변을 받기 위해 function call 형태 지정.
        functions=[
            {
                "name": "generate_fairytale",
                # 없어도 되긴 함
                "description": "Generate a fairytale in Korean with four parts: 발단, 전개, 절정, 결말",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "발단": {"type": "string", "description": "Introduction of the story"},
                        "전개": {"type": "string", "description": "Development of the story"},
                        "절정": {"type": "string", "description": "Climax of the story"},
                        "결말": {"type": "string", "description": "Conclusion of the story"}
                    },
                    "required": ["발단", "전개", "절정", "결말"]
                }
            }
        ],
        function_call={"name": "generate_fairytale",
                       "arguments": "{\"발단\": \"\", \"전개\": \"\", \"절정\": \"\", \"결말\": \"\"}"}
    )

    # 운용 편의성을 위해 json output format을 강제했지만, json 포맷대로 UI에 띄우면 굉장히 보기 싫음
    # 그래서 생성된 문장 전체를 저장하는 문자열 하나를 만들고, 생성될 때 마다 해당 문자열에 저장
    # json format에 맞춰서 replace로 json을 위한 양식은 삭제해가며 출력(파싱할 때 써야하니 output은 건드리면 안됨)
    output = ""
    for chunk in response:
        output_change = output.replace('''{"발단":"''', '')
        output_change = output_change.replace('''"}''', '')
        if chunk.choices[0].delta.function_call is None:
            continue
        output += str(chunk.choices[0].delta.function_call.arguments)
        sys.stdout.write("\r" + output_change)
        sys.stdout.flush()

    output_dict = {"role": "assistant", "content": output}
    input_messages.append(output_dict)
    return input_messages


# 이렇게 하면 입력 + 답변이 자연스럽게 저장됨.
# class 만들어서 인스턴스 형태로 관리하거나 뭐...... 뭔가 적절한 방법이 있겠죠?
# messages = stream(messages)