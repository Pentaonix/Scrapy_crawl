import scrapy
import os
import json

class TestIPSpider(scrapy.Spider):
    name = "test_ip"

    def start_requests(self):
        url = 'http://httpbin.org/ip'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.text)