# -*- coding: utf-8 -*-
import sqlite3
import os

def createDB():
    conn = sqlite3.connect("movie.db")
    c = conn.cursor()
    c.execute('''
            create table urlInfo(id text, url text, time datetime, count int)
            ''')
    c.execute('''
            create table movie(id text, name text, desc text, info text, img text, tags text)
            ''')
    conn.commit()
    conn.close()

def InsertMovie(id, name, desc, info, img, tags):
    if not os.path.exists("movie.db"):
        createDB()
    
    conn = sqlite3.connect("movie.db")
    c = conn.cursor()
    sql = 'insert into movie values(?, ?, ?, ?, ?, ?)' # % (id, name, desc, info, img, tags)

    c.execute(sql, (id, name, desc, info, img, tags))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    InsertMovie("abc", "qwe", "renren", "www", "oiu", "")
            
