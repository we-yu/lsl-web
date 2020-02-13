import os
from pymongo import MongoClient
import datetime
import urllib.parse
import setting # For enviroment load

import sqlite3
from pprint import pprint

DB_LOCATION = '../db/lsl.db'
DB_USER = setting.mongoUser
DB_PASS = setting.mongoPass

print("Setting.DB_USER :", DB_USER)
print("Setting.DB_PASS :", DB_PASS)

# RDB       MongoDB
# database  database
# table     collection
# row       document
# column	field
# index     index
# p key     _id

# https://www.tech-tech.xyz/mongodb-sql.html

def GetMongoDBClient():
    mongoPath = "mongodb://mongo:27017/"
    mongoUsr = DB_USER
    mongoPass = DB_PASS
    mongoUsr = urllib.parse.quote_plus(mongoUsr)
    mongoPass = urllib.parse.quote_plus(mongoPass)
    accessor = "mongodb://%s:%s@mongo:27017/" % (mongoUsr, mongoPass)
    print("accessor = " + accessor)

    client = MongoClient(accessor)

    return client

# try:
#     conn = MongoClient()
#     print("Connected successfully!!!")
# except:
#     print("Could not connect to MongoDB")


def MongoDBConnectionTest():


    client = GetMongoDBClient()

    # Get DB "test_database" from MongoDB / Create DB on MongoDB if not found
    db = client.test_database
    # db = client['test_database'] # same as above

    # Call collection / Create if nothing
    collection = db.test_collection
    # collection = db['test_collection']

    # Drop(Delete) all records
#    collection.drop()

    # json style document
    # post = {
    #     "author": "Mike",
    #     "text": "My first blog post",
    #     "tags": ["mongodb", "python", "pymongo"],
    #     "date": datetime.datetime.utcnow()
    # }
    # Insert document to collection
    # result1 = collection.insert_one(post)
    # Select from collection
    # print("==Find Collection==")
    # print(collection.find_one())

    # In case of multiple insert
    new_posts = [{"author": "Mike",
                  "text": "Another post!",
                  "tags": ["bulk", "insert"],
                  "date": datetime.datetime(2009, 11, 12, 11, 14)},
                 {"author": "Eliot",
                  "title": "MongoDB is fun",
                  "text": "and pretty easy too!",
                  "date": datetime.datetime(2009, 11, 10, 10, 45)}]
    print(type(new_posts[0]) , type(new_posts))
    pprint(new_posts)
    result2 = collection.insert_many(new_posts)
    print("==Find Collection==")
    finds = collection.find()
    # for find in finds :
    #     pprint(find)

    return

def ConnectSQLite_FetchAll(tableName) :
    conn = sqlite3.connect(DB_LOCATION)
    cursor = conn.cursor()

    q =\
    '''
    SELECT * FROM %s;
    ''' % (tableName)

    cursor.execute(q)
    dbResult = cursor.fetchall()
    # pprint(dbResult)

    conn.commit()

    # database_check(cursor)

    conn.close()

    return dbResult

def MigrateFromSQLtoMongoDB(database='lslMongoDB', tableName='') :
    lslClient = GetMongoDBClient()
    lsldb = lslClient[database]
    lslColl = lsldb[tableName]
    lslColl.drop()

    listData = ConnectSQLite_FetchAll(tableName)

    dicList = []
    if(tableName == "sticker_list") :
        for line in listData:
            newDic = {"id": line[0], "url": line[1], "title": line[2], "comment": line[3]}
            dicList.append(newDic)

    if(tableName == "sticker_detail") :
        for line in listData:
            # newDic = {"parent_id": line[0], "child_id": line[1], "url_L": line[2], "url_M": line[3], "url_S": line[4]}
            newDic = {"id": {"parent":line[0], "child":line[1]}, "iconUrl":{"L":line[2], "M":line[3], "S":line[4]}}
            dicList.append(newDic)

    retVal = lslColl.insert_many(dicList)

    return lsldb, lslColl

# MongoDBConnectionTest()
# print("================")
# listData = ConnectSQLite_FetchAll("sticker_list")
# # pprint(listData)
#
# print("= Migrated Mongo DB ===============")
#
# lslClient = GetMongoDBClient()
#
# # DataBase
# lsldb = lslClient.lslMongoDB
#
# # Table
# stiList = lsldb.sticker_list
#
# # Drop
# stiList.drop()
#
# print(type(listData[0]) , type(listData))
# pprint(listData)
#
# # Convert from tuple to "List of Dic"
# dicList = []
# for line in listData :
#     newDic = {"id":line[0], "url":line[1], "title":line[2], "comment":line[3]}
#     dicList.append(newDic)
#
# pprint(dicList)
#
# result2 = stiList.insert_many(dicList)

limit = 5
count = 0

dbName = "lslMongoDB"
#--------------------------------------------------------------
tableName = "sticker_list"
migratedDB, listCol = MigrateFromSQLtoMongoDB(dbName, tableName)

print("==Find Collection Migrated : %s==" % tableName)
finds = listCol.find()
for find in finds:
    pprint(find)
    print()
    count = count + 1
    if (count == limit) : break;

count = 0

print()
print()

#--------------------------------------------------------------
tableName = "sticker_detail"
migratedDB, detailCol = MigrateFromSQLtoMongoDB(dbName, tableName)

print("==Find Collection Migrated : %s==" % tableName)
finds = detailCol.find()
for find in finds:
    pprint(find)
    print()
    count = count + 1
    if (count == limit) : break;

count = 0

print()

print("== SELECT/Find test ==")
findVal = detailCol.find_one({"id.parent":1252985})
pprint(findVal)



# { "_id" : ObjectId("54996816e0035c426fd71b2c"),
#   "id" : 1,
#   "name" : "kuwa_tw",
#   "nosql" : "mongodb",
#   "price" : 10,
#   "created_at" : "2014-12-23T21:14:39+0900" }
