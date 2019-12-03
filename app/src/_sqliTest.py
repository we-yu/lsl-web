# coding: UTF-8
import sqlite3
# import DBController

from pprint import pprint

# https://www.htmllifehack.xyz/entry/2018/08/03/231351

# Use SQLite by Python3

# Create DB file.
con = sqlite3.connect('../db/lsl.bak.db', isolation_level=None)

print(con)
# Create cursor-object
cursor = con.cursor()

try:
    ### Read DATA --------------------------------------------------------------------------------------

    # conn = sqlite3.connect('sample.db')
    # cursor = conn.cursor()

    query = 'SELECT * FROM sticker_list'
    # Get all data from executed query (Type = List)
    cursor.execute(query)
    fAll = cursor.fetchall()
    pprint(fAll)

    print('---')

    # Get data 1 by 1
    cursor.execute(query)
    fOne = cursor.fetchone()
    pprint(fOne)
    fOne = cursor.fetchone()
    pprint(fOne)
    fOne = cursor.fetchone()
    pprint(fOne)

    print('---')

    # Get data as non-list (with loop)
    cursor.execute(query)
    for row in cursor :
        print(row[0], row[1], row[2])

    print('---')

except sqlite3.Error as e :
    print('sqlite3.Error occurred : ', e.args[0])
