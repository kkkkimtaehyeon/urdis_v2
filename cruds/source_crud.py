from bson import ObjectId

from db import source_collection
from schemas import Source


def fetch_source(id: str):
    source = source_collection.find_one({'_id': ObjectId(id)})
    return {
        "id": str(source["_id"]),
        "prompt": source["prompt"]
    }


def fetch_all_sources():
    sources = source_collection.find()
    return [{
        "id": str(source["_id"]),
        "prompt": source["prompt"]
    } for source in sources]


def save_source(source: Source):
    saved_source = source_collection.insert_one(dict(source))
    return str(saved_source.inserted_id)


def remove_source(id: str):
    try:
        source_collection.delete_one({'_id': ObjectId(id)})
    except Exception as e:
        print(f"delete source collection error: {e}")
