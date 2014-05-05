# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqldb

class DoubancrawlPipeline(object):
    def process_item(self, item, spider):
	
	sqldb.InsertMovie(item['id'], item['name'], item['desc'], item['info'], item['img'], item['tags'])
        return item
