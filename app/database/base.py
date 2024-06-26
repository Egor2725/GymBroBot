from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from app.config import db


class Base(BaseModel):
    _collection: AsyncIOMotorClient

    @classmethod
    async def count(cls):
        num = await cls._collection.count_documents({})
        return num

    @classmethod
    async def get(cls, id: int):
        obj = await cls._collection.find_one({'_id': id})
        return cls(**obj) if obj else None

    @classmethod
    async def find(cls, **kwargs):
        obj = await cls._collection.find_one(dict(kwargs))
        return cls(**obj) if obj else None

    @classmethod
    async def get_all(cls):
        objs = cls._collection.find()
        return [cls(**u) async for u in objs]

    @classmethod
    async def update(cls, id: int, **kwargs):
        await cls._collection.find_one_and_update({'_id': id}, {'$set': kwargs})
        return await cls.get(id)

    @classmethod
    async def create(cls, **kwargs):
        if '_id' not in kwargs:
            kwargs["_id"] = await cls.count() + 1
        obj = cls(**kwargs)
        obj = await cls._collection.insert_one(obj.model_dump(by_alias=True))
        return await cls.get(obj.inserted_id)

    @classmethod
    async def bulk_create(cls, objects: list['Base']):
        # TODO create bulk method
        raise NotImplementedError
    @classmethod
    async def delete(cls, id: int):
        await cls._collection.find_one_and_delete({'_id': id})
        return True

    @classmethod
    def set_collection(cls, collection: str):
        cls._collection = db[collection]
