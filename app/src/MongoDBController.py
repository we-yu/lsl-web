from pymongo import MongoClient
import datetime
import urllib.parse
import setting # For enviroment load
from pprint import pprint

DB_USER = setting.mongoUser
DB_PASS = setting.mongoPass

print("Kicked Mongo Ctrl", DB_USER, DB_PASS)


class MongoDBController :
    @property
    def mongoClient(self):
        return self.__client
    @mongoClient.setter
    def mongoClient(self, value):
        self.__client = value

    def __init__(self):
        print('Call ' + self.__class__.__name__ + ' Constructor')
        self.mongoClient = self.GetMongoDBClient()

    # Get connection to MongoDB container
    def GetMongoDBClient(self):
        mongoUsr = DB_USER
        mongoPass = DB_PASS
        mongoUsr = urllib.parse.quote_plus(mongoUsr)
        mongoPass = urllib.parse.quote_plus(mongoPass)
        # "mongodb" = Fixed phrase
        # "@mongo" = Depend on Container define. (not "container_name")
        accessor = "mongodb://%s:%s@mongo:27017/" % (mongoUsr, mongoPass)

        print(accessor)
        client = MongoClient(accessor)

        return client

    def Insert():
        return
    def Update():
        return
    def Remove():
        return

    def MongoDBFetchTest(self):
        dbName = "lslMongoDB"
        tableName = "sticker_list"

        lslClient   = self.mongoClient
        lsldb       = lslClient[dbName]
        lslColl     = lsldb[tableName]

        findVal = lslColl.find_one({"id.parent":1252985})
        print("== Fetched Value ==")
        pprint(findVal)

mongoCtrl = MongoDBController()
mongoCtrl.MongoDBFetchTest()

