import sqlite3
import sys
from pprint import pprint

# State class
class SQLiteController():

    DB_LOCATION = '../db/lsl.db'

    # DB File
    @property
    def con(self):
        return self.__con
    @con.setter
    def con(self, value):
        self.__con = value

    # Cursor object
    @property
    def cursor(self):
        return self.__cursor
    @cursor.setter
    def cursor(self, value):
        self.__cursor = value

    dbtype = ""

    def __init__(self):
        self.dbtype = "SQLite"
        co, cr = self.GetConnectCursor()

    def GetConnectCursor(self):
        con = self.CheckCreateDB()
        cur = con.cursor()
        return con, cur

    # Get Target DB file. If not exit, Create & Get.
    def CheckCreateDB(self):
        relativePath = SQLiteController.DB_LOCATION

        # print("relativePath", relativePath)

        con = sqlite3.connect(relativePath)
        return con

    def Json2Query(self, jsonquery):
        return

    def Create(self, q, opt=[]):
        print(self.dbtype, sys._getframe().f_code.co_name, q)

    def Read(self, q, opt=[]):
        print(self.dbtype, sys._getframe().f_code.co_name, q)
        # {'collection': 'sticker_detail', 'projection': {'id': 1, 'title': 1}, 'selection': {'id.parent': 1162635},
        #  'sort': {'enable': 1, 'order': 0}}
        # 'SELECT local_id FROM sticker_detail WHERE parent_id=%s ORDER BY local_id' % (parentID)

        q_select    = "SELECT"
        q_from      = "FROM"
        q_where     = "WHERE"

        q_select    += " " + q["projection"][0]
        q_from      += " " + q["collection"]

        for dicKey in q["selection"].keys() :
            keyVal = q["selection"][dicKey]
            where_cond = "(%s = %s)" % (dicKey, keyVal)

        q_where     += " " + where_cond

        q_order = ""
        if (q["sort"]["enable"]):
            q_order  = "ORDER BY"
            sort_param = "ASC" if q["sort"]["order"]["direction"] == 1 else "DESC"
            q_order += " " + q["sort"]["order"]["key"] + " " + sort_param

        squery = q_select + " " + q_from + " " + q_where + " " + q_order

        print("squery =", squery)

        co, cr = self.GetConnectCursor()

        cr.execute(squery)

        type = "ABC"
        if type == 'count':
            dbResult = cr.fetchone()
            dbResult = int(dbResult[0])
        else:
            dbResult = cr.fetchall()
        co.close()

        for find in dbResult:
            pprint(find)

    def Update(self, q, opt=[]):
        print(self.dbtype, sys._getframe().f_code.co_name, q)

    def Delete(self, q, opt=[]):
        print(self.dbtype, sys._getframe().f_code.co_name, q)
