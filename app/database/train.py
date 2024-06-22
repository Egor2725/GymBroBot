from pydantic import Field
from datetime import datetime

from .base import Base


class User(Base):
    id: int = Field(default_factory=int, alias="_id")
    name: str
    username: str

    @classmethod
    async def get_or_create(cls, id: int, name: str, username: str | None) -> ('User', bool):
        user = await cls.get(id)
        if not user:
            user = await cls.create(_id=id, name=name, username=username)
            return user, True
        return user, False


class Exercise(Base):
    id: int = Field(default_factory=int, alias='_id')
    name: str
    train_type: str
    train_part: str | None

    @classmethod
    async def get_or_create(cls, name: str, train_type: str, train_part: str | None = None) -> ('Exercise', bool):
        exercise = await cls.find(name=name)
        if not exercise:
            exercise = await cls.create(name=name, train_type=train_type, train_part=train_part)
            return exercise, True
        return exercise, False

    @classmethod
    async def filter_by_train_type_and_part(cls, train_type: str | None, train_part: str | None):
        search = {}

        if train_part:
            search['train_part'] = train_part

        if train_type:
            search['train_type'] = train_type

        objs = cls._collection.find(search)
        return [cls(**u) async for u in objs]


class Train(Base):
    id: int = Field(default_factory=int, alias="_id")
    exercise_id: int
    user_id: int
    weight: float
    times: int
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)

    def __str__(self):
        return f'{self.exercise_id}, {self.weight}, {self.times}, {self.created.date()}: {self.created.time()}'

    @classmethod
    async def get_all_by_user_id(cls, id: int):
        objs = cls._collection.find({'user_id': id})
        return [cls(**u) async for u in objs]
        

User.set_collection('users')
Exercise.set_collection('exercise')
Train.set_collection('trains')
