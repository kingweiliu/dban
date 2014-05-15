# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
import md5
import re
import locale
import os
from doubancrawl.items import qtfyItem

def IsMoviePageUrl(url):
    if re.match('http:\/\/www\.qtfy30\.cn\/[^\/]+\/\d+\.html', url) != None:
        return True
    return False

class qtfySpider(Spider):
    name = "qtfy"
    allowed_domains = ["http://www.qtfy30.cn/"]
    start_urls = (
        'http://www.qtfy30.cn/',
        )		
    id_gen = md5.new()
    url_visited = {}
    url_scheduled = {}
   
    def parse(self, response):
        sel = Selector(response)
        









if __name__ == '__main__':
    urls = ['http://www.qtfy30.cn/ysyl/11007.html',
            'http://www.qtfy30.cn/ysyl/10955.html',
            'http://www.qtfy30.cn/category/rjxz',
            'http://www.qtfy30.cn/hjxz/11002.html',
            'http://www.qtfy30.cn/category/hjxz']
    for url in urls:
        print IsMoviePageUrl(url)

    
