# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback
import MySQLdb
import redis  #键值数据库
import logging
import scrapy_redis_mongodb.settings as settings
from scrapy.utils.project import get_project_settings
import pymongo
from scrapy.exceptions import DropItem

class RedisPipeline(object):
    def __init__(self):
        self.redis_table = settings.MY_REDIS  # 选择表
        self.redis_db = redis.Redis(host=settings.REDIS_SERVER, port=settings.REDIS_PORT, db=settings.REDIS_DB)  # redis数据库连接信息

    def process_item(self, item, spider):
        if self.redis_db.exists(item['url']):
            raise DropItem('%s id exists!!' % (item['url']))
        else:
            self.redis_db.lpush(self.redis_table, item['url'])
        return item


class  MgdbPipeline(object):
    '''mogodb连接方式'''
    # 连接方式一
    # def __init__(self):
    #     self.conn = pymongo.MongoClient("mongodb://{}:{}/".format(settings.MONGODB_SERVER,settings.MONGODB_PORT))
    #     self.db = self.conn[settings.MONGODB_DB] #选择数据库
    #     self.MG_table = self.db[settings.MONGODB_COLLECTION] #选择表
    def __init__(self):
        self.mongo_config = get_project_settings().get(settings.MONGODB_URI)
        self.conn = pymongo.MongoClient(self.mongo_config)
        self.db = self.conn[settings.MONGODB_DB]  # 选择数据库
        self.MG_table = self.db[settings.MONGODB_COLLECTION]  # 选择表

    def process_item(self, item, spider):
        if self.site_item_exist(item):
            self.MG_table.insert(dict(item))
            logging.debug("Question added to MongoDB database!")
            # log.msg("Question added to MongoDB database!", level=log.DEBUG, spider=spider)
            '''
            Scrapy 提供 5 层 logging 级别：
            CRITICAL - 严重错误(critical)
            ERROR - 一般错误(regular errors)
            WARNING - 警告信息(warning messages)
            INFO - 一般信息(informational messages)
            DEBUG - 调试信息(debugging messages)     本程序用的就是DEBUG

            '''
        else:
            raise DropItem("{} is exist".format(item['url']))
        return item

    def site_item_exist(self, item):
        if self.MG_table.find_one({"url": item['url']}):
            return False
        else:
            return True