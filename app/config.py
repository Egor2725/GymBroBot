import os
from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv(dotenv_path=join(dirname(__file__), "..", "local.env"))

TOKEN = os.getenv("TOKEN")
