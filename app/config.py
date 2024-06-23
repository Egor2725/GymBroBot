import os
from os.path import join, dirname
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv(dotenv_path=join(dirname(__file__), "..", "local.env"))
load_dotenv(dotenv_path=join(dirname(__file__), ".", "local.env"))


TOKEN = os.getenv("TOKEN")

MONGO_USER = os.getenv('MONGO_USER', default='admin')
MONGO_PASS = os.getenv('MONGO_PASS', default='admin')
MONGO_HOST = os.getenv('MONGO_HOST', default='mongo')
MONGO_PORT = os.getenv('MONGO_PORT', default=27017)
MONGO_URL = f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/'


client = AsyncIOMotorClient(MONGO_URL)
db = client["test"]
