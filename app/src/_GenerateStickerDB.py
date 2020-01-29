# coding: UTF-8
import sqlite3
from pprint import pprint

DB_LOCATION = '../db/lsl.db'

def create_connection(db_file) :
    try :
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e :
        print(e)
    finally :
        conn.close()
    return conn

def get_sticker_list():
    q =\
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

def get_sticker_detail() :
    q =\
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

def database_check(cursor) :
    # -----------------------------------------------------
    data = [
        (7554, 'https://www/aaa/bbb', 'Sti_Alpha', '/usr/bin/aaa'),
        (54968521, 'https://www/aaa/ccc', 'Sti_Beta', '/usr/bin/bbb'),
        (89841, 'https://www/aaa/b3b', 'Sti_Thehta', '/usr/bin/ccc'),
        (999, 'https://www/aaa/ggg', 'Sti_Bravo', '/usr/bin/ddd')
    ]
    query = 'INSERT INTO sticker_list VALUES(?, ?, ?, ?)'
    cursor.executemany(query, data)

    data = [
        (333, 53123, 'https://www/aaa/L', 'https://www/aaa/M', 'https://www/aaa/S'),
        (333, 32441, 'https://www/bbb/L', 'https://www/bbb/M', 'https://www/bbb/S')
    ]
    query = 'INSERT INTO sticker_detail VALUES(?, ?, ?, ?, ?)'
    cursor.executemany(query, data)

    conn.commit()
    # -----------------------------------------------------
    query = 'SELECT * FROM sticker_list ORDER BY id'
    cursor.execute(query)
    fAll = cursor.fetchall()
    pprint(fAll)
    print('---')
    query = 'SELECT * FROM sticker_detail ORDER BY local_id'
    cursor.execute(query)
    fAll = cursor.fetchall()
    pprint(fAll)
    print('---')
    # -----------------------------------------------------
    return

# if __name__ == '__main__' :
# conn = create_connection(DB_LOCATION)
conn = sqlite3.connect(DB_LOCATION)
cursor = conn.cursor()

cursor.executescript(get_sticker_list())
cursor.executescript(get_sticker_detail())

conn.commit()

# database_check(cursor)

conn.close()