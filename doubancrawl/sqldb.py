# -*- coding: utf-8 -*-
import sqlite3


def createDB(conn):
    conn = sqlite3.connect("movie.db")
    c = conn.cursor()
    c.execute('''
            create table urlInfo(id text, url text, time datetime, count int)
            ''')
    c.execute('''
            create table movie(id text, name text, desc text, info text, img text, tags text)
            ''')

def InsertMovie(id, name, desc, info, img, tags):
    conn = sqlite3.connect("movie.db")
    c = conn.cursor()
    sql = 'insert into movie values(?, ?, ?, ?, ?, ?)' # % (id, name, desc, info, img, tags)

    c.execute(sql, (id, name, desc, info, img, tags))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    InsertMovie("abc", "qwe", "renren", "www", "oiu", "")
            
