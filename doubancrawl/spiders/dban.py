# -*- coding: utf-8 -*-
from scrapy.spider import Spider

class DbanSpider(Spider):
    name = "dban"
    allowed_domains = ["douban.com"]
    start_urls = (
        'http://www.douban.com/',
        )
    
    def parse(self, response):
	filename = response.url.split("/")[-2]
	print filename
	
	filecontent = response.body.decode('utf-8', 'ignore').encode('gbk', 'ignore')
	print "body:%s" % response.body
	print "ljw:%s" % filecontent
	open(filename, 'wb').write(response.body)
         
