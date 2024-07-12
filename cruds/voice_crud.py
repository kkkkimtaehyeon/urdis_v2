from typing import List, Dict

from bson import ObjectId
from fastapi import UploadFile

from db import voice_collection, story_collection
from aws import S3Manager

s3_manager = S3Manager()


def fetch_voices() -> List[Dict]:
    voices = voice_collection.find()

    return voices


def create_voice(name: str, image_file: UploadFile, sample_prompt: str, model: str):
    image = s3_manager.upload_on_s3(image_file)

    # TODO: sample_prompt를 tts로 오디오 파일로 변환 후 s3업로드
    dummy_audio_sample = "test_audio_sample" + sample_prompt

    voice = voice_collection.insert_one({
        "name": name,
        "image": image,
        "audio_sample": dummy_audio_sample,
        "voice_model": model,
    })

    return str(voice.inserted_id)


def voice_on_story(story_id: str, voice_id: str):
    story = story_collection.find_one({"_id": ObjectId(story_id)})
    voice = voice_collection.find_one({"_id": ObjectId(voice_id)})
    voice_model = voice["voice_model"]

    story_contents = story["contents"]
    # TODO: voice_model로 story_contents tts하고 s3에 업로드

    contents_voices = [f"voice_url{i}" for i in range(10)]

    story_collection.update({"_id": ObjectId(story_id)}, {"$set": {"contents_voices": contents_voices}})

