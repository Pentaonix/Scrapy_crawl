# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
from crawl4websites.settings import USER_AGENT
from crawl4websites.headers import HEADERS

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(HEADERS)
        if ua:
            request.headers.setdefault('User-Agent', ua)
            
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        pass
        request.meta['proxy'] = USER_AGENT