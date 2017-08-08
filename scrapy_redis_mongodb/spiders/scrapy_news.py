# -*- coding: utf-8 -*-
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
import scrapy
import time
import json
from ..items import ScrapyRedisMongodbItem
class XpathRule(object):
    total_page = "//div[@class='pagenav']/a/text()"
    urlist = "//table[@class='tablelist']//tr[@class='even']//a/@href|//table[@class='tablelist']//tr[@class='odd']//a/@href"

class CctvSpider(scrapy.Spider):
    name = "tencent"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_redis_mongodb.pipelines.RedisPipeline': 300
        }}
    start_urls = ['http://hr.tencent.com/position.php']

    def parse(self, response):
        try:
            total_page = response.xpath(XpathRule.total_page).extract()[-2]
        except:
            return
        for p in xrange(int(total_page)):
            url = "http://hr.tencent.com/position.php?&start={}#a".format((p)*10)
            yield scrapy.Request(url, self.parse_detail)

    def parse_detail(self, response):
        urls = response.xpath(XpathRule.urlist).extract()
        for url in urls:
            item = ScrapyRedisMongodbItem()
            item['url'] = "http://hr.tencent.com/"+url
            yield item


