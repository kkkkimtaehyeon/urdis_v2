from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
MONGODB_URL = os.getenv('MONGODB_URL')
client = MongoClient(MONGODB_URL)

db = client.story_generator_db

source_collection = db['source_collection']
story_collection = db['story_collection']
page_collection = db['page_collection']

