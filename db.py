from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

_ = load_dotenv(find_dotenv())
MONGODB_URL = os.getenv('MONGODB_URL')
client = MongoClient(MONGODB_URL)
# client = AsyncIOMotorClient(MONGODB_URL)
db = client.story_generator_db

story_collection = db['story_collection']
story_meta_collection = db['story_meta_collection']
voice_collection = db['voice_collection']

