import sqlite3
import os

__strsql_create = [
          "create table movie(mid text, name text, url text, desc text, info text, img text)",
          "create table downloadlinks(mid text, title text, href text)"
          ]

__str_insert_movie = "insert into movie values(?, ?, ?, ?, ?, ?)"
__str_insert_link = "insert into downloadlinks values(?, ?, ?)"

def createDb(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    for str in __strsql_create:
        c.execute(str)
    conn.commit()
    conn.close()

def insertMovie(mid, name, url, desc, info, img, links):
    dbname = "qtfy.db"
    if not os.path.exists(dbname):
        createDb(dbname)
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute(__str_insert_movie, (mid, name, url, desc, info, img))
    for lk in links:
        c.execute(__str_insert_link, (mid, lk["title"], lk["href"]))
    conn.commit()
    conn.close()



