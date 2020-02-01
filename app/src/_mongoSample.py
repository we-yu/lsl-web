from pymongo import MongoClient
import datetime

client = MongoClient('mongodb', 27117)

# Get DB "test_database" from MongoDB / Create DB on MongoDB if not found
db = client.test_database
# db = client['test_database'] # same as above

# Call collection / Create if nothing
collection = db.test_collection
# collection = db['test_collection']

# Drop(Delete) all records
collection.drop()

# json style document
post = {
    "author" : "Mike",
    "text" : "My first blog post",
    "tags" : ["mongodb", "python", "pymongo"],
    "date" : datetime.datetime.utcnow()
}

# Insert document to collection
# result1 = collection.insert_one(post)

# In case of multiple insert
# new_posts = [{"author": "Mike",
#               "text": "Another post!",
#               "tags": ["bulk", "insert"],
#               "date": datetime.datetime(2009, 11, 12, 11, 14)},
#              {"author": "Eliot",
#               "title": "MongoDB is fun",
#               "text": "and pretty easy too!",
#               "date": datetime.datetime(2009, 11, 10, 10, 45)}]
# result2 = collection.insert_many(new_posts)

# Select from collection
print("==Find Collection==")
# print(collection.find_one())
