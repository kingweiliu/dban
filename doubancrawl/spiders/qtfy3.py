import scrapy
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response
#from doubancrawl.items import DoubancrawlItem
from doubancrawl.items import qtfyItem
import md5

from scrapy.utils.request import request_fingerprint

class Qtfy3Spider(CrawlSpider):
    name = 'qtfy3'
    allowed_domains = ['www.qtfy30.cn']
    start_urls = ['http://www.qtfy30.cn']

    rules = (
        Rule(SgmlLinkExtractor(r"ysyl\/\d+.html$"), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(r"mjxz\/\d+.html$"), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(r"hjxz\/\d+.html$"), callback='parse_item', follow=True),        
        Rule(SgmlLinkExtractor(r"page\/d+"))
    )

    def isDownloadLink(self, href):
        return href[0:10] == "thunder://" or href[-4:] == ".mp4" or href[-5:] == ".rmvb" \
            or href[:22] == "http://kuai.xunlei.com" \
            or href[:20] == "http://pan.baidu.com"

    def parse_item(self, response):
        #i = DoubancrawlItem()
        print "ljw: *****************"
        print response.url
        item = qtfyItem()
        #tp = md5.new(response.url)
        #item["id"] = tp.hexdigest()
        item["id"] = request_fingerprint(response.request)
        item["url"] = response.url
        item["name"] = response.xpath("//h2/text()").extract()[0]
        entry = response.xpath('//div[@class="entry"]/p')
        
        item["desc"] = entry[0].xpath("text()").extract()[0]
         
        infos = entry[1].xpath("node()").extract()
        if len(infos) < 3:
            infos = entry[2].xpath("node()").extract()

        item["info"] = reduce((lambda x, y: x+y), infos)
        item["img"] = entry.xpath('img/@src').extract()[0]
        
        lnks = entry.xpath('a')
        lkret = []
        for ln in lnks:
            href = ln.xpath("@href").extract()[0]
            
            if not self.isDownloadLink(href):
                continue
            title = ln.xpath("text()").extract()[0]
            lkret.append({"title":title, "href":href})
        item["links"] = lkret
        #print item
        #inspect_response(response, self)
        yield item
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        #return i


        
