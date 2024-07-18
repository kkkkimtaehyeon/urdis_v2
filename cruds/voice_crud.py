from typing import List, Dict

from bson import ObjectId
from fastapi import UploadFile

from db import voice_collection, story_collection
from aws import S3Manager
from ai_modules.tts_work import text_to_speech

s3 = S3Manager()


def fetch_voices() -> List[Dict]:
    voices = voice_collection.find()

    return voices


def create_voice(name: str, image_file: UploadFile, sample_prompt: str, model: str):
    image = s3.upload_on_s3(image_file)

    audio = text_to_speech(text=sample_prompt, voice_name=model)
    uploaded_audio_url = s3.upload_audio_on_s3(audio, filename=name)

    voice = voice_collection.insert_one({
        "name": name,
        "image": image,
        "audio_sample": uploaded_audio_url,
        "voice_model": model,
    })

    return str(voice.inserted_id)


def attach_voice_on_story(story_id: str, voice_id: str):
    story = story_collection.find_one({"_id": ObjectId(story_id)})
    voice = voice_collection.find_one({"_id": ObjectId(voice_id)})

    voice_model = voice["voice_model"]
    contents_list = story["contents"]

    #페이지의 내용을 음성으로 변홚
    contents_voices = []

    for content in contents_list:
        audio = text_to_speech(text=content, voice_name=voice_model)
        uploaded_audio_url = s3.upload_audio_on_s3(audio, str(story['_id']))
        contents_voices.append(uploaded_audio_url)

    # 더미데이터
    #contents_voices = [f"voice_url{i}" for i in range(10)]

    story_collection.update_one(
        {"_id": ObjectId(story_id)},
        {"$set": {
            "contents_voices": contents_voices,
            "voice_model": voice_model
            }
        }
    )

