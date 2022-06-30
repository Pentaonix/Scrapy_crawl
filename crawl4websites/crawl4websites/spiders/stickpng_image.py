import scrapy
import os
import json
import glob

from crawl4websites.items import LinkItem

class StickPngImageSpider(scrapy.Spider):
    name = "stickpng_image"

    def start_requests(self):
        output_dir = '/data/1019_crawl_img/crawl_images/stickpng'
        animal_photo_categories = ['animals', 'memes', 'nature']
        animal_drawing_categories = ['cartoons', 'clothes', 'comics-and-fantasy', 'food', 'games', 'holidays', 'icons-logos-emojis', 'miscellaneous', 'people', 'religion']
        person_drawing_categories = ['science', 'sports', 'transport', 'world-landmarks']
        for category in person_drawing_categories:
            child_cats = glob.glob('/device_5tb/1019_crawl_img/crawl_images/stickpng/{}/*'.format(category))
            for child_cat in child_cats:
                print('Start crawl image links of {}'.format(child_cat))
                links = [line.strip() for line in open(os.path.join(child_cat, 'links.txt'))]
                if os.path.exists(os.path.join(child_cat, 'links_img.txt')):
                    crawled_links = [line.strip().split(',')[0].split('//www.')[1] for line in open(os.path.join(child_cat, 'links_img.txt'))]
                    links_img = [line.strip().split(',')[1] for line in open(os.path.join(child_cat, 'links_img.txt'))]
                    for link in links:
                        if link.split('//')[1] not in crawled_links:
                            yield scrapy.Request(url=link.strip(), callback=self.parse_big_link)
                else:
                    with open(os.path.join(output_dir, category, child_cat, 'links_img.txt'), 'w') as links_file:
                        pass
                    for link in links:
                        yield scrapy.Request(url=link.strip(), callback=self.parse_big_link)
                    
    def parse_big_link(self, response):
        output_dir = '/device_5tb/1019_crawl_img/crawl_images/stickpng/stickpng'
        homepage = 'https://stickpng.com'
        url = response.request.url
        
        child_cat_url = url.split('/img/')[1]
        cat = child_cat_url.split('/')[0]
        child_cat = child_cat_url.split('/')[1]
        
        link_list = response.xpath('//section[@class="clearfix wide"]/div[@class="image"]//img/@src').getall()
        link = link_list[0]
        with open(os.path.join(output_dir, cat, child_cat, 'links_img.txt'), 'a+') as links_file:
            links_file.write('{},{}\n'.format(url, link))