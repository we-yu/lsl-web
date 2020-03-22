import os
from os.path import join, dirname
from dotenv import load_dotenv
from Logger import Logger

ENV_FILE_NAME = ".mongoEnv"

# True : Show warning message
load_dotenv(verbose=True)

# Get target .env file path. By relative path from this file.
dotenv_path = join(dirname(__file__), "../env/", ENV_FILE_NAME)
# Load target .env file.
load_dotenv(dotenv_path)

# Defined values in .env file, assign to variable.
allowedDB = os.environ.get("ALLOWED_DB")
# mongoName = os.environ.get("ENV_MONGO_INITDBNAME")
# mongoUser = os.environ.get("ENV_MONGO_INITDB_ROOT_USERNAME")
# mongoPass = os.environ.get("ENV_MONGO_INITDB_ROOT_PASSWORD")
mongoName = os.environ.get("MONGO_INITDB_DATABASE")
mongoUser = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
mongoPass = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
mongoPort = os.environ.get("MONGO_CONNECTPORT")
# Sample usage in other python file
# =============================================
# import setting # For enviroment load
#
# DB_USER = setting.mongoUser
# DB_PASS = setting.mongoPass

# AlloedDB, single string value. "DB names" splited by " "(space). Split and make it as array.
availDBs = allowedDB.split()


Logger(mongoName, mongoUser, mongoPass, mongoPort)