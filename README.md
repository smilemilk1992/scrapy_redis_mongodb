# scrapy_redis_mongodb
基于Python+scrapy+redis的分布式爬虫实现框架

#project start
运行run.py

#scrapy_news.py
主要功能是抓取种子url，保存到redis

#redis_mongo.py
主要是从redis里面读url，解析数据保存到mongodb
（拓展到其他机器，都是从redis里面读url）
