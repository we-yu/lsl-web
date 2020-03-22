import sys
from pymongo import MongoClient
import datetime
import urllib.parse
from pprint import pprint
import setting # For enviroment load

import ast
import json
from pprint import pprint

from Logger import Logger
from Logger import ListLogger

DB_NAME = setting.mongoName
DB_USER = setting.mongoUser
DB_PASS = setting.mongoPass
DB_PORT = setting.mongoPort

# State class
class MongoDBController():
    dbtype = ""

    @property
    def mongoClient(self):
        return self.__client
    @mongoClient.setter
    def mongoClient(self, value):
        self.__client = value

    @property
    def mongoDatabase(self):
        return self.__collection
    @mongoDatabase.setter
    def mongoDatabase(self, value):
        self.__collection = value

    def __init__(self):
        Logger('Call ' + self.__class__.__name__ + ' Constructor')
        Logger("MongoDB Log")
        mongoName = DB_NAME
        mongoName = urllib.parse.quote_plus(mongoName)
        self.dbtype = "MongoDB"
        self.mongoClient = self.GetMongoDBClient()
        self.mongoDatabase = mongoName

    # Get connection to MongoDB container
    def GetMongoDBClient(self):
        mongoUsr = DB_USER
        mongoPass = DB_PASS
        mongoPort = DB_PORT
        mongoUsr = urllib.parse.quote_plus(mongoUsr)
        mongoPass = urllib.parse.quote_plus(mongoPass)
        mongoPort = urllib.parse.quote_plus(mongoPort)
        # "mongodb" = Fixed phrase
        # "@mongo" = Depend on Container define. (not "container_name")
        accessor = "mongodb://%s:%s@mongo:%s/" % (mongoUsr, mongoPass, mongoPort)

        Logger("accessor =", accessor)
        client = MongoClient(accessor)
        Logger("client =", client)

        return client

    def Create(self, q, opt=[]):
        Logger(self.dbtype, sys._getframe().f_code.co_name, q)

        lslCol = self.GetTargetCollection(q["collection"])

        result = lslCol.insert(q["insert"])
        return result

    def Read(self, q, opt=[]):
        Logger(self.dbtype, sys._getframe().f_code.co_name, "Function")
        Logger(q)

        # Connecting to target collection (From collection name)
        lslCol = self.GetTargetCollection(q["collection"])

        Logger("lslCol", lslCol)

        # Select Query for MongoDB
        # If key not defined, Use empty/0 value.
        search_select   = q.get("projection",   {}) # SELECT
        search_cond     = q.get("selection",    {}) # WHERE
        search_limit    = q.get("limit",        0)  # LIMIT

        # Connect and send query
        finds = lslCol
        finds = finds.find(search_cond, search_select)  # SELECT & WHERE
        finds = finds.limit(search_limit)               # LIMIT

        # ORDER
        sort_query = ""
        sort_key = q.get("sort", {}).get("key")
        sort_direction = q.get("sort", {}).get("direction")
        # If "key" and "direction" defined in query, Do sorting.
        if (sort_key and sort_direction) :
            sort_query = [(sort_key, sort_direction)]
            finds = finds.sort(sort_query)

        # Convert from Cursor to List
        # Logger("Finds a =")
        # for find in finds:
        #     pprint(find)

        retVal = list(finds)

        # If this query is for counting, Return only counted amount
        if(q.get("count")) :
        # if(("count" in q) and q["count"]) :
            retVal = finds.count()                      # COUNT

        # query = "lslCol.find(%s, %s).limit(%s).sort(%s)" % (search_cond, search_select, search_limit, sort_query)
        # Logger("Query =", query)

        return retVal

    def Update(self, q, opt=[]):
        Logger(self.dbtype, sys._getframe().f_code.co_name, q)

        lslCol = self.GetTargetCollection(q["collection"])

        result = lslCol.update(q["selection"], q["update"])
        return result


    def Delete(self, q, opt=[]):
        Logger(self.dbtype, sys._getframe().f_code.co_name, q)

        lslCol = self.GetTargetCollection(q["collection"])

        result = lslCol.remove(q["remove"])
        return result

    # Get collection handler from name
    def GetTargetCollection(self, colName):
        lslClient   = self.mongoClient
        lsldb       = lslClient[self.mongoDatabase]
        tgtCol      = lsldb[colName]
        return tgtCol
