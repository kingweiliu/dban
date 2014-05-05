# Scrapy settings for doubancrawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'doubancrawl'

SPIDER_MODULES = ['doubancrawl.spiders']
NEWSPIDER_MODULE = 'doubancrawl.spiders'
#EXTENSIONS = {
#    'scrapy.contrib.corestats.CoreStats': None
#    }

#DOWNLOADER_MIDDLEWARES = {
#    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None
#    }
ITEM_PIPELINES = {
	'doubancrawl.pipelines.DoubancrawlPipeline': 300
}

DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 1
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
	
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'doubancrawl (+http://www.yourdomain.com)'
