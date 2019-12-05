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
        print('Call ' + self.__class__.__name__ + ' Constructor')
        # Get DB file
        # self.con = self.CheckCreateDB()
        # self.cursor = self.con.cursor()
        # Need close
        # self.con.close()

    def GetConnectCursor(self):
        con = self.CheckCreateDB()
        cur = con.cursor()
        return con, cur

    # Get Target DB file. If not exit, Create & Get.
    def CheckCreateDB(self):
        relativePath = DBCtrl.DB_LOCATION

        con = sqlite3.connect(relativePath)
        return con

    def Create(self, query, data=None, type=None):
        co, cr = self.GetConnectCursor()
        if type == 'many':
            dbResult = cr.executemany(query, data)
        else:
            dbResult = cr.execute(query)
        co.commit()
        co.close()

        return dbResult

    def Read(self, query, type=None):

        co, cr = self.GetConnectCursor()

        cr.execute(query)

        if type == 'count':
            dbResult = cr.fetchone()
            dbResult = int(dbResult[0])
        else:
            dbResult = cr.fetchall()
        co.close()

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
