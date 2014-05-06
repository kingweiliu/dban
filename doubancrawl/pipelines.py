# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqldb
from items import qtfyItem
import qtfylib

class DoubancrawlPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, qtfyItem):  
            qtfylib.insertMovie(item["id"], item["name"], item["url"], item["desc"], item["info"], item["img"], item["links"])
            return item
        sqldb.InsertMovie(item['id'], item['name'], item['desc'], item['info'], item['img'], item['tags'])
        return item
