import scrapy
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response
from scrapy.selector import Selector
from doubancrawl.items import MovieItem
import md5

from scrapy.utils.request import request_fingerprint

class douban2Spider(CrawlSpider):
    name = 'douban2'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com']

    rules = (
        Rule(SgmlLinkExtractor(r"subject\/\d+\/$"), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(r"subject\/\d+\/\?from"), callback='parse_item', follow=True),  
    )

    def parse_item(self, response):
        sel = Selector(response)
        mi = MovieItem()
        shorturl = response.url[response.url.find("subject/"):]
        
        urlparts = shorturl.split("/")
        mi['id'] = urlparts[1]
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

        return mi


        
