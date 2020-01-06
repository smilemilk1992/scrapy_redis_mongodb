# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyRedisMongodbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()

class data_redis_mongodb(scrapy.Item):
    PostURL = scrapy.Field()
    PostId=scrapy.Field()
    RecruitPostName = scrapy.Field()
    LocationName = scrapy.Field()
    BGName = scrapy.Field()
    CategoryName = scrapy.Field()
    Responsibility=scrapy.Field()
    Requirement=scrapy.Field()
    LastUpdateTime=scrapy.Field()



