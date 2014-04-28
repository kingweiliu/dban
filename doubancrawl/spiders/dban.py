# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
import md5
import re
import locale
import os

def isMovieUrl(url):
    if re.match('.*\/\/movie\.douban\.com\/subject\/\d+\/.*', url) != None:
        return True
    return False

UT_MOVIE = 1
UT_MOVIE_OTHER = 2
UT_NOMOVIE = 3

def urlType(url):
    paths = url.split('/')
    if len(paths)>4:
        if paths[0] == "http:" and len(paths[1]) == 0 and paths[2] == "movie.douban.com":
            if paths[3] == "subject":
                if re.match('\d+', paths[4]) != None:
                    if paths[5] == "" or paths[5][0:5]== "?from":
                        return UT_MOVIE
        else:
            return UT_NOMOVIE   #not movie.douban.com
    return UT_MOVIE_OTHER
##    
##                
##            
##    
##    if re.match('http:\/\/movie\.douban\.com\/subject\/\d+', url) != None:
##        return UT_MOVIE
    return 0

class DbanSpider(Spider):
    name = "dban"
    allowed_domains = ["douban.com"]
    start_urls = (
        'http://movie.douban.com/',
        )		
    id_gen = md5.new()
    url_visited = {}
    url_scheduled = {}
   
    def parse(self, response):
        
        self.id_gen.update(response.url)
        tmfilename = self.id_gen.hexdigest()
        if tmfilename in self.url_visited:
            return
        open(os.path.join("page", tmfilename), 'wb').write(response.body)
        self.url_visited[tmfilename] = response.url

        sel = Selector(response)
        links = sel.xpath("//a[@href and text()]")
        
##        flink = open("lnk.txt", "w")
        print "locale:", locale.getdefaultlocale()
        for si in links:
            href = si.xpath("@href").extract()[0]
            text = si.xpath("text()").extract()[0]

            ut = urlType(href)
            if ut == UT_NOMOVIE:
                continue
            else:
                self.id_gen.update(href)
                id = self.id_gen.hexdigest()
                if id in self.url_scheduled:
                    continue
                self.url_scheduled[id] = href
                if ut != UT_MOVIE:
                    yield Request(href)
                    continue
                else:
                    suffixIdx = href.find("?")
                    if suffixIdx != -1 :
                        href = href[0:suffixIdx]
                        self.id_gen.update(href)
                        id = self.id_gen.hexdigest()
                        self.url_scheduled[id] = href
                    yield Request(href, callback=self.parseMoviePage)                                   
##                    flink.write(text.encode('utf-8', 'ignore')+"\n")
##                    flink.write(href.encode('utf-8', 'ignore') + "\n")
##        print "ljw cnt: ", len(links)
##        flink.close()

    def parseMoviePage(self, response):
        print "parseMoviePage"
        pass

    
if __name__ == "__main__":
    a= ['http://movie.douban.com/category/', 'http://movie.douban.com/subject/25715087/', 'http://www.jb51.net/article/17849.htm',
        'http://movie.douban.com/people/79362936/',
        'http://movie.douban.com/subject/6973460/?from=showing']
    for url in a:
        if urlType(url) == UT_MOVIE:
            print url
