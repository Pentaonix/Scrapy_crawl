import scrapy
import os
import json
import glob

from crawl4websites.items import LinkItem

class StickPngImageSpider(scrapy.Spider):
    name = "pngmart_image"

    def start_requests(self):
        animal_photo_categories = ['animals']
        animal_drawing_categories = ['cartoons', 'holidays-png', 'love', 'fantasy', 'internet-meme']
        person_drawing_categories = ['gaming', 'internet-png', 'fictional-characters', 'people', 'education-science']
        for category in person_drawing_categories:
            child_cats = glob.glob('/device_5tb/1019_crawl_img/crawl_images/pngmart/{}/*'.format(category))
            for child_cat in child_cats:
                print('Start crawl image links of {}'.format(child_cat))
                category = child_cat.split('/')[-2]
                child_category = child_cat.split('/')[-1]
                links = [line.strip() for line in open(os.path.join(child_cat, 'links.txt'))]
                if os.path.exists(os.path.join(child_cat, 'links_img.txt')):
                    crawled_links = [line.strip().split(',')[0] for line in open(os.path.join(child_cat, 'links_img.txt'))]
                    links_img = [line.strip().split(',')[1] for line in open(os.path.join(child_cat, 'links_img.txt'))]
                    for link in links:
                        if link not in crawled_links:
                            yield scrapy.Request(url=link.strip(),
                                                 callback=self.parse_big_link,
                                                 cb_kwargs=dict(cat=category, child_cat=child_category))
                else:
                    for link in links:
                        yield scrapy.Request(url=link.strip(), 
                                             callback=self.parse_big_link,
                                             cb_kwargs=dict(cat=category, child_cat=child_category))
                    
    def parse_big_link(self, response, cat, child_cat):
        output_dir = '/device_5tb/1019_crawl_img/crawl_images/pngmart'
        url = response.request.url
        
        link = response.xpath('//div[@class="entry-content"]/p/a/@href').getall()[0]
        with open(os.path.join(output_dir, cat, child_cat, 'links_img.txt'), 'a+') as links_file:
            links_file.write('{},{}\n'.format(url, link))