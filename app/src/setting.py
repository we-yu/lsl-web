import os
from os.path import join, dirname
from dotenv import load_dotenv

ENV_FILE_NAME = ".mongoEnv"

# True : Show warning message
load_dotenv(verbose=True)

# Get target .env file path. By relative path from this file.
dotenv_path = join(dirname(__file__), "../env/", ENV_FILE_NAME)
# Load target .env file.
load_dotenv(dotenv_path)

# Defined values in .env file, assign to variable.
mongoUser = os.environ.get("ENV_MONGO_INITDB_ROOT_USERNAME")
mongoPass = os.environ.get("ENV_MONGO_INITDB_ROOT_PASSWORD")

# Sample usage in other python file
# =============================================
# import setting # For enviroment load
#
# DB_USER = setting.mongoUser
# DB_PASS = setting.mongoPass
