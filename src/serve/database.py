from typing import Any, Mapping
import pymongo
from pymongo import MongoClient
from src.config import settings


def create_database_client() -> MongoClient[Mapping[str, Any] | Any]:
    mongo_uri = settings.mongo_db_uri
    client = pymongo.MongoClient(mongo_uri)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client
