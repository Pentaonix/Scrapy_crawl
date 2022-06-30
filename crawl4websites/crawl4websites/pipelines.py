# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy

class ImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['big_img_link'])

    def item_completed(self, results, item, info):
        print(results)
        image_paths = ['{}/{}/{}'.format(item['cat'], item['child_cat'], x['path']) for ok, x in results if ok]
        print(image_paths)
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

class Crawl4WebsitesPipeline:
    def process_item(self, item, spider):
        return item
