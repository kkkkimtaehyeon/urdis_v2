import requests
import json
import base64

from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


def text_to_speech(text, voice_name):  # text, voice_name(선택 음성), output_file(출력할 MP3 파일 이름)
    # TTS 요청을 위한 엔드포인트 (여기로 text 보내라)
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_API_KEY}"

    # 요청 페이로드
    data = {
        "input": {
            "text": text
        },
        "voice": {
            "languageCode": "ko-KR",  # 한국어 음성
            "name": voice_name,  # 특정 한국어 목소리
            "ssmlGender": "FEMALE" if "A" in voice_name or "B" in voice_name else "MALE"
        },
        "audioConfig": {
            "audioEncoding": "MP3"  # MP3 형식으로 음성 데이터 반환
        }
    }

    # 요청 헤더
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }

    # API 요청 보내기
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 응답 데이터 확인
    if response.status_code == 200:
        response_data = response.json()
        audio_content = response_data['audioContent']

        audio_binary = base64.b64decode(audio_content)

        print("음성 데이터가 성공적으로 생성되었습니다.")
        return audio_binary
    else:
        print("오류가 발생했습니다:", response.text)
        return None


# # 테스트를 위해 동화 텍스트 입력
# text = "그린나래, 우리는 생성AI를 활용한 동화를 생성해주는 프로젝트를 진행중이에요 안녕하세요 내 이름은 김주혁 탐정이죠. 오늘 우리는 행복한 이야기를 만들어볼거에요 지금 부터 잘 보세요 계속 만들어 질거에요 아아아아아아 힘들지만 버텨죠"
#
# # 사용할 음성 목록
# voices = [
#     ("ko-KR-Standard-A", "test_A.mp3"),
#     ("ko-KR-Standard-B", "test_B.mp3"),
#     ("ko-KR-Standard-C", "test_C.mp3"),
#     ("ko-KR-Standard-D", "test_D.mp3")
# ]
#
# for voice_name, output_file in voices:
#     text_to_speech(text, voice_name, output_file)
