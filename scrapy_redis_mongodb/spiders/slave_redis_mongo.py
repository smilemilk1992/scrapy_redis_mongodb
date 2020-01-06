# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from ..items import data_redis_mongodb
import re
import time
import json
import scrapy
class MySpider(RedisSpider):
    '''slave端'''
    name = 'redis'
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_redis_mongodb.pipelines.MgdbPipeline': 300
        }}
    redis_key = 'myspider:start_urls' #从redis里面读url

    def parse(self, response):
        id=re.search("\d+",response.url).group(0)
        url="https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp={}&postId={}&language=zh-cn".format(int(time.time())*1000,id)
        yield scrapy.Request(url,callback=self.getDetail)

    def getDetail(self,response):
        json_data=json.loads(response.body)
        datas=json_data.get("Data")
        item = data_redis_mongodb()
        item["PostId"]=datas.get("PostId")
        item["RecruitPostName"]=datas.get("RecruitPostName")
        item["LocationName"]=datas.get("LocationName")
        item["BGName"]=datas.get("BGName")
        item["CategoryName"]=datas.get("CategoryName")
        item["Responsibility"]=datas.get("Responsibility")
        item["Requirement"]=datas.get("Requirement")
        item["LastUpdateTime"]=datas.get("LastUpdateTime")
        item["PostURL"]="http://careers.tencent.com/jobdesc.html?postId={}".format(datas.get("PostId"))
        yield item