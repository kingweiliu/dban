# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
import md5
import re
import locale
import os
from doubancrawl.items import MovieItem
from scrapy.shell import inspect_response
from scrapy.utils.request import request_fingerprint

def isMovieUrl(url):
    if re.match('.*\/\/movie\.douban\.com\/subject\/\d+\/.*', url) != None:
        return True
    return False

def isMovieDomain(url):
    if re.match("http:\/\/movie\.douban\.com.*", url) != None:
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

class DbanSpider(Spider):
    name = "dban"
    allowed_domains = ["movie.douban.com"]
    start_urls = (
        'http://movie.douban.com/',
        #'http://www.baidu.com/',
        )


        
   
    def parse(self, response):
        print "******************************"
        mi = MovieItem()
##        mi['id'] = "abc"  #request_fingerprint(response.request)
##        mi['name'] = "de f"   # sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()[0]
##        mi['desc'] = "desc"
##        mi['tags'] = "tags"
##        mi["info"] = "into"
##        mi['img'] = "img"
##        print "end*************"
##        return mi
    
        sel = Selector(response)
        links = sel.xpath("//a[@href and text()]")
        for si in links:
            href = si.xpath("@href").extract()[0]
            text = si.xpath("text()").extract()[0]
            if not isMovieDomain(href):
                continue            
                   

            ut = urlType(href)
            if ut != UT_MOVIE:
                yield Request(href)                
            else:
##                suffixIdx = href.find("?")
##                if suffixIdx != -1 :
##                    href = href[0:suffixIdx]
##                    urlid = self.urlId(href)                    
   
                yield Request(href, callback=self.parseMoviePage)                                   


    def parseMoviePage(self, response):
        sel = Selector(response)
        mi = MovieItem()
        mi['id'] = request_fingerprint(response.request)
        mi['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()[0]
        mi['desc'] = ""
        for n in sel.xpath('//*[@id="link-report"]/span[1]/node()').extract():
            mi['desc'] += n
        
        mi['img'] = sel.xpath('//*[@id="mainpic"]/a/img/@src').extract()[0]
        strTags = sel.xpath('//*[@class="tags-body"]/a/text()').extract()
        mi['tags'] = ""
        for str in strTags:
            mi['tags'] += str+","
        mi["info"] = ""
        for info in sel.xpath('//*[@id="info"]/node()').extract():
            mi['info'] += info
        #inspect_response(response, self)
        yield mi
        #return self.parse(response)
    
if __name__ == "__main__":
    a= ['http://movie.douban.com/category/',
        'http://movie.douban.com/subject/25715087/',
        'http://www.jb51.net/article/17849.htm',
        'http://movie.douban.com/people/79362936/',
        'http://movie.douban.com/subject/6973460/?from=showing']
    for url in a:
        if urlType(url) == UT_MOVIE:
            print url
