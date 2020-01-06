# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ScrapyRedisMongodbItem
class XpathRule(object):
    total_page = "//div[@class='pagenav']/a/text()"
    urlist = "//table[@class='tablelist']//tr[@class='even']//a/@href|//table[@class='tablelist']//tr[@class='odd']//a/@href"

class CctvSpider(scrapy.Spider):
    '''master端'''
    name = "tencent"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_redis_mongodb.pipelines.RedisPipeline': 300,
            'scrapy_redis.pipelines.RedisPipeline': 400
        }}

    flag='https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1578294726673&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'

    def start_requests(self):
        page=1
        yield scrapy.Request(self.flag.format(page),callback=self.parse,meta={"page":page})

    def parse(self, response):
        json_data=json.loads(response.body)
        posts=json_data.get("Data",{}).get("Posts")
        for post in posts:
            item = ScrapyRedisMongodbItem()
            PostId=post.get("PostId")
            postUrl = "http://careers.tencent.com/jobdesc.html?postId={}".format(PostId)
            item['url']=postUrl
            yield item
        if posts is not None:
            page=response.meta["page"]+1
            yield scrapy.Request(self.flag.format(page), callback=self.parse, meta={"page": page})




