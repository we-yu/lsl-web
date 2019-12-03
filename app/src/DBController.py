# coding: UTF-8

import sqlite3
import pprint

import os

class DBCtrl:
    DB_LOCATION = 'db/lsl.db'

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

    def __init__(self):
        # print('Call ' + self.__class__.__name__ + ' Constructor')
        # Get DB file
        self.con = self.CheckCreateDB()
        # Generate cursor object
        # self.cursor = self.con.cursor()
        self.cursor = self.con.cursor()
        # query = 'SELECT * FROM sticker_list'
        # # Get all data from executed query (Type = List)
        # self.cursor.execute(query)
        self.con.close()

    def GetConnectCursor(self):
        con = self.CheckCreateDB()
        cur = con.cursor()
        return con, cur

    # Get Target DB file. If not exit, Create & Get.
    def CheckCreateDB(self):
        relativePath = DBCtrl.DB_LOCATION

        con = sqlite3.connect(relativePath)
        return con

        # if os.path.exists(relativePath) == False :
        #     con = self.InitializeDB(relativePath)
        # else :
        #     con = sqlite3.connect(relativePath)
        #     self.cursor = con.cursor()
        # return con

    def InitializeDB(self, dbPath):
        con = sqlite3.connect(dbPath)

        self.cursor = con.cursor()
        self.cursor.executescript(self.get_sticker_list())
        self.cursor.executescript(self.get_sticker_detail())

        return con

    def get_sticker_list(self):
        q = \
            '''
            DROP TABLE IF EXISTS sticker_list;
            CREATE TABLE sticker_list
            (
                id INTEGER PRIMARY KEY,         -- Sticker's unique number : https://store.line.me/stickershop/product/3104873/ja -> 3104873
                url VARCHAR(256),               -- All url text
                title VARCHAR(256),             -- Sticker's title (Replaced '/' and ' ')
                stored_directory VARCHAR(256)   -- Downloaded Sticker's stored location (local path)
            );
            '''
        return q

    def get_sticker_detail(self):
        q = \
            '''
            DROP TABLE IF EXISTS sticker_detail;
            CREATE TABLE sticker_detail
            (
                parent_id INTEGER,              -- sticker_list.id
                local_id INTEGER,               -- https://stickershop.line-scdn.net/stickershop/v1/sticker/32258568/iPhone/sticker@2x.png -> 32258568
                url_sticker_l VARCHAR(256),     -- Larger size sticker's url
                url_sticker_m VARCHAR(256),     -- Middle size sticker's url
                url_sticker_s VARCHAR(256),     -- Small  size sticker's url
                PRIMARY KEY (parent_id, local_id)   -- Define composite key (Double id)
            );
            '''
        return q

    def Create(self, query, data=None, type=None):
        if type == 'many':
            dbResult = self.cursor.executemany(query, data)
        else:
            dbResult = self.cursor.execute(query)
        self.con.commit()
        return dbResult

    def Read(self, query, type=None):

        # cn = sqlite3.connect(relativePath, isolation_level=None)
        # print(cn)
        # # Create cursor-object
        # csr = cn.cursor()

        co, cr = self.GetConnectCursor()
        # query = 'SELECT count(*) FROM sticker_list'
        # # Get all data from executed query (Type = List)
        # cr.execute(query)
        # fAll = cr.fetchall()
        # print("IN READ :", fAll)
        # co.close() aa

        cr.execute(query)

        if type == 'count':
            dbResult = cr.fetchone()
            dbResult = int(dbResult[0])
        else:
            dbResult = cr.fetchall()

        return dbResult

    def Update(self):
        return

    def Delete(self):
        return

    def ExecuteQuery(self, con, q):
        try:
            print('Query is [', q, ']')
        except sqlite3.Error as e:
            print('sqlite3.Error occurred : ', e.args[0])
