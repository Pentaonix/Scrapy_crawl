# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkItem(scrapy.Item):
    homepage = scrapy.Field()
    cat = scrapy.Field()
    child_cat = scrapy.Field()
    big_img_link = scrapy.Field()
