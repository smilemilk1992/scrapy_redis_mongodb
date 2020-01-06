from scrapy import Request, Spider


class TestSpider(Spider):
    name = 'test'
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_redis.pipelines.RedisPipeline': 400
        }
    }
    base_url = 'https://www.baidu.com/s?wd='

    def start_requests(self):
        for i in range(100):
            url = self.base_url + str(i)
            yield Request(url, callback=self.parse)

        # Here contains 10 duplicated Requests
        for i in range(10,110):
            url = self.base_url + str(i)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        self.logger.debug('Response of ' + response.url)