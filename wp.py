# -*- coding: utf-8 -*-
import xmlrpclib
import sys
import datetime
import sqlite3
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
import string
from douban.service import DoubanService

wp = Client('http://192.168.147.128/wordpress/xmlrpc.php', 'liujingwei', 'ljw')

class qtfy_db:

    def __init__(self, name):
        self.dbname = name

    def __exec(self, sql, param):
        print param
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        sqlret = c.execute(sql, param)
        ret = sqlret.fetchall()
        conn.commit()
        conn.close()
        return ret
        
    def get_movielnks(self, mid):
        lnks = self.__exec("select title, href from downloadlinks where mid = ?", tuple([mid]))
        return lnks

def gen_webpage(content, info, imgsrc, links):
    ftemp = open("moviepage.tmpl")
    str = string.Template(ftemp.read())
    d = {'content':content, 'info':info, 'imgsrc':imgsrc}
    ret = str.substitute(d)
    print ret
    for lk in links:
        ret += u"<a href='%s'>%s</a><br/>" % (lk[1], lk[0])
    return ret

def insertPostFromDB():
    conn = sqlite3.connect('qtfy.db')
    c = conn.cursor()
    idx = 0
    db = qtfy_db('qtfy.db')
    for row in c.execute("select mid, name, url, desc, info, img from movie"):
        if idx>2:
            break
        post = WordPressPost()
        print row[0]
        post.title =  row[1]
        lk = db.get_movielnks(row[0])
        post.content = gen_webpage(row[3], row[4], row[5], lk) # row[3] + row[4]
        post.terms_names={'post_tag':['liu', 'jing']}
        post.post_status = "publish"
        idx += 1
        print wp.call(NewPost(post))
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    #db = qtfy_db('qtfy.db')
    #print db.get_movielnks('75af1af1fcab573e899d6d8ab260369f089ffffb')
    insertPostFromDB()
