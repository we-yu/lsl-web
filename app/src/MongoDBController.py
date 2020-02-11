from pymongo import MongoClient
import datetime
import urllib.parse
import setting # For enviroment load

DB_USER = setting.mongoUser
DB_PASS = setting.mongoPass

# Get connection to MongoDB container
def GetMongoDBClient():
    mongoUsr = DB_USER
    mongoPass = DB_PASS
    mongoUsr = urllib.parse.quote_plus(mongoUsr)
    mongoPass = urllib.parse.quote_plus(mongoPass)
    # "mongodb" = Fixed phrase
    # "@mongo" = Depend on Container define. (not "container_name")
    accessor = "mongodb://%s:%s@mongo:27017/" % (mongoUsr, mongoPass)

    client = MongoClient(accessor)

    return client

def Insert():
    return

def Update():
    return

def Remove():
    return
