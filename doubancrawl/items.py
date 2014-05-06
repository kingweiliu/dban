# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MovieItem(Item):
    # define the fields for your item here like:

    id = Field()
    name = Field()
    desc = Field()
    info = Field()
    img = Field()
    tags = Field()
    
    

class qtfyItem(Item):
    id = Field()
    url = Field()
    name = Field()
    desc = Field()
    info = Field()
    img = Field()
    links = Field()    
