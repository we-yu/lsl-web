import MongoDBController
import SQLiteController

# DB management class
# Working by State pattern.
from pprint import pprint
from Logger import Logger
from Logger import ListLogger

# Context class
class DBContext:
    AVAILABLE_DB = ("SQLITE", "MONGODB")
    dbSelect = {}
    valid_db = []
    selectedOne = ""
    option = []

    def __init__(self):
        # Load "Available" DB names. On this case, MongoDB and SQLite.
        self.valid_db = self.GetValidDBs()
        Logger(type(self.valid_db), self.valid_db)

        # Create instance of DBcontrol objects (This objects should be have same methods)
        # self.dbSelect['sqlite']     = SQLiteController.SQLiteController()
        self.dbSelect['mongodb']    = MongoDBController.MongoDBController()

    def GetValidDBs(self):
        # List of available DB names, Change to lowercase. (Mapping with Lambda)
        dbs = list(map(lambda x: x.lower(), self.AVAILABLE_DB))
        return dbs

    def change_state(self, selectDB):
        # Just in case, Change to lowercase given DBname.
        selectDB = selectDB.lower()

        # If given DB not supported, Make expection.
        if (selectDB not in self.valid_db):
            raise ValueError("change_state method must be in {}".format(self.valid_db))

        # Change "STATE" to given DB.
        # After this, Called function from given DB class.
        #   ex, Call Create() func -> [MongoDB].Create() func or [SQLite].Create() func.
        self.selectedONE = selectDB
        self.state = self.dbSelect[selectDB]

    def Create(self, q):
        return self.state.Create(q, self.option)

    def Read(self, q):
        return self.state.Read(q, self.option)

    def Update(self, q):
        return self.state.Update(q, self.option)

    def Delete(self, q):
        return self.state.Delete(q, self.option)

###################################################################################################
### Below, Functions for Debug ####################################################################
###################################################################################################

def CreateTest(obj) :
    inquery = {
        "collection": "_sandbox",
        "insert": {
            "location": 'Hatyai',
            "name": 'Saint George',
            "personal": {
                "sex": 'm',
                "age": 61,
                "language": 'Spanish'
            }
        }
    }
    result = obj.Create(inquery)
    Logger("CREATE : at State result =", result)

    return

def CreateBulkTest(obj) :
    inquery = {
        "collection": "_sandbox",
        "insert": [
            {
                "location": 'Hatyai',
                "name": 'Saint George',
                "personal": {
                    "sex": 'm',
                    "age": 61,
                    "language": 'Spanish'
                }
            },
            {
                "location": 'Korat',
                "name": 'Sawarat Sponches',
                "personal": {
                    "sex": 'f',
                    "age": 45,
                    "language": 'Oriental'
                }
            }

        ]
    }
    Logger("Bulk Create :", inquery)
    result = obj.Create(inquery)
    Logger("CREATE BULK : at State result =", result)

    return

def ReadTest(obj):
    chosenDBtype = "sqlite"
    # obj.change_state(chosenDBtype)

    # inquery = {
    #     "collection": "sticker_detail",
    #     "projection": ["local_id"],
    #     "selection": {
    #         "parent_id":1162635
    #     },
    #     "sort": {
    #         "enable": 1,
    #         "order": {
    #             "key":"local_id",
    #             "direction":-1
    #         }
    #     }
    # }
    # Logger("inquery =", type(inquery))

    query = "foofoo"
    # obj.Create(query)
    # obj.Read(inquery)
    # obj.Update(query)
    # obj.Delete(query)
    # --------------------
    Logger("---")
    # inquery = {
    #     "collection": "sticker_detail",
    #     "projection": {
    #         "_id":0
    #         # ,"id.child":1
    #         # ,"id.parent":1
    #     },
    #     "selection": {
    #         "id.parent":1252985
    #     },
    #     "sort": {
    #         "key":"id.child",
    #         "direction":-1
    #
    #     },
    #     "limit": 5
    # }

    inquery = {
        "collection": "sticker_list",
        "projection": {
            "id": 1,
            "title": 1
        },
        "selection": {},
        "sort": {
            "key": "title",
            "direction": 1
        },
        "limit": 0
    }

    # Logger("inquery =", type(inquery))

    query = "baabaa"
    finds = obj.Read(inquery)
    Logger("Read test result")
    for find in finds:
        pprint(find)

    return

def UpdateTest(obj):

    inquery = {
        "collection": "_sandbox",
        # Update target record condition
        "selection": {
            "name":"Asuka Tanaka"
        },
        # Update contents
        "update": {
                "$set": {
                    "personal.age":32
                }
        }
    }

    result = obj.Update(inquery)
    Logger("UPDATE : at State result =", result)

    return

def DeleteTest(obj):

    inquery = {
        "collection": "_sandbox",
        "remove": {
            "personal.age":{"$gte":30}
        }
    }
    result = obj.Delete(inquery)
    Logger("Delete : at State result =", result)

    return

def CountTest(obj):

    inquery = {
        "collection": "sticker_list",
        "selection": {
            "id":8173575
        },
        "count": 1
    }
    # Logger("inquery =", type(inquery))
    findCount = obj.Read(inquery)
    Logger("list count =", findCount)

    inquery = {
        "collection": "sticker_detail",
        "selection": {
            "id.parent":1206683
        },
        "count": 1
    }
    # 1293651

    # Logger("inquery =", type(inquery))
    findCount = obj.Read(inquery)
    Logger("detail count =", findCount)
    # for find in finds:
    #     pprint(find)

    return

def IsExistInDB(obj, parentID) :
    inquery = {
        "collection": "sticker_list",
        "selection": {
            "id":parentID
        },
        "count": 1
    }
    listCount = obj.Read(inquery)

    inquery = {
        "collection": "sticker_detail",
        "selection": {
            "id.parent":parentID
        },
        "count": 1
    }
    detailCount = obj.Read(inquery)

    Logger("Sticker", parentID, "Count is", listCount, "/", detailCount)

    return bool(listCount and detailCount)

# Delete target All sticker data from list, detail collection (clean up)
def Util_DeleteAllSticker(obj, parentID):
    inquery = {
        "collection": "sticker_list",
        "remove": {
            "id":parentID
        }
    }
    result = obj.Delete(inquery)

    inquery = {
        "collection": "sticker_detail",
        "remove": {
            "id.parent":parentID
        }
    }
    result = obj.Delete(inquery)
    return

def main():
    # Create context instance
    ctxObj = DBContext()
    chosenDBtype = "mongodb"
    ctxObj.change_state(chosenDBtype)

    # --------------------
    # CreateTest(ctxObj)
    ReadTest(ctxObj)
    # UpdateTest(ctxObj)
    # DeleteTest(ctxObj)

    # CountTest(ctxObj)
    # Logger("1293651 is Exist? ", IsExistInDB(ctxObj, 1293651))
    # Logger("5858634 is Exist? ", IsExistInDB(ctxObj, 5858634))
    # CreateBulkTest(ctxObj)
    # --------------------
    return

    family = {
        "Smith" : {
            "father" : "Michel",
            "mother" : "Maria"
        },
        "Stewart" : {
            "father" : "John",
            "mother" : "Alissa",
            "children" : {
                "first" : "Tabasa",
                "second" : "Robart",
                "third" : "Gablier"
            }
        }
    }
    pprint(family)
    Logger("Smith :", family.get("Smith"))
    Logger("Hazel :", family.get("Hazel"))
    Logger("Smith.children :", family.get("Smith", {}).get("children"))
    Logger("Stewart.children :", family.get("Stewart", {}).get("children"))
    Logger("Hazel.children :", family.get("Hazel", {}).get("children"))



if __name__ == "__main__":
    main()

