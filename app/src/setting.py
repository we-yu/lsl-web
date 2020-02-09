import os
from os.path import join, dirname
from dotenv import load_dotenv

ENV_FILE_NAME = ".mongoEnv"

print("== Setting.py ==")
load_dotenv(verbose=True)
# print("r path = ", dirname(__file__))

dotenv_path = join(dirname(__file__), "../env/", ENV_FILE_NAME)
# print("dotenv_path = ", dotenv_path)
load_dotenv(dotenv_path)

mongoUser = os.environ.get("ENV_MONGO_INITDB_ROOT_USERNAME")
mongoPass = os.environ.get("ENV_MONGO_INITDB_ROOT_PASSWORD")

print(mongoUser, mongoPass)

