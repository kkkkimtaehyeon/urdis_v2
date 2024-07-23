from typing import Dict, List

from fastapi import APIRouter, Form, UploadFile, File

from cruds.voice_crud import fetch_voices, create_voice, attach_voice_on_story

router = APIRouter(tags=['voice'])


@router.get("/api/voices")
async def get_voices() -> List[Dict[str, str]]:
    voices = fetch_voices()

    return [{
        "id": str(voice["_id"]),
        "name": voice["name"],
        "image": voice["image"],
        "audio": voice["audio_sample"]
    } for voice in voices]


@router.post("/api/voices/new")
async def post_new_voice(name: str = Form(...),
                         image: UploadFile = File(...),
                         sample_prompt: str = Form(...),
                         voice_model: str = Form(...)
                         ):
    voice_id = create_voice(name, image, sample_prompt, voice_model)

    return voice_id


@router.post("/api/stories/{story_id}/voices/{voice_id}")
async def apply_voice_on_story(story_id: str, voice_id: str = None):  # 선택적 voice_id
    attach_voice_on_story(story_id, voice_id)

    return story_id
