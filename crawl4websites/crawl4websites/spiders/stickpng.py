import scrapy
import os
import json

class StickPngSpider(scrapy.Spider):
    name = "stickpng"
    
    def start_requests(self):
        urls = [line.strip() for line in open('/mnt/c/Users/QuangND/data/1019_crawl_img/crawl_images/stickpng/link_child_cat.txt', 'r')]
#         urls = ['https://www.stickpng.com/cat/animals/cats']
        for url in urls:
            cat = url.strip().split('/')[-3]
            child_cat = url.strip().split('/')[-2]
            if os.path.exists(os.path.join('/mnt/c/Users/QuangND/data/1019_crawl_img/crawl_images/stickpng', cat, child_cat, 'links.txt')):
                print('Skip category {} child catergory {}'.format(cat, child_cat))
            else:
                print('Crawl {}'.format(url))
                yield scrapy.Request(url=url, callback=self.parse)
                
    def parse(self, response):
        homepage = 'http://stickpng.com'
        output_dir = '/mnt/c/Users/QuangND/data/1019_crawl_img/crawl_images/stickpng'
        url = response.request.url
        print(url)
        child_cat_url = url.split('?page=')[0]
        cat = child_cat_url.split('/')[-3]
        child_cat = child_cat_url.split('/')[-2]
        
        if not os.path.exists(os.path.join(output_dir, cat)):
            os.mkdir(os.path.join(output_dir, cat))
        if not os.path.exists(os.path.join(output_dir, cat, child_cat)):
            os.mkdir(os.path.join(output_dir, cat, child_cat))
            
        if 'page=' not in url:
            page_info = response.xpath('//section[@id="pagination"]/@data-pagination').getall()[0]
            page_info_dict = json.loads(page_info)
            nbr_page = int(page_info_dict['pages'])
            current_page = int(page_info_dict['current'])
            if nbr_page > 1:
                for page_number in range(2, nbr_page + 1):
                    yield scrapy.Request(url='{}?page={}'.format(url, page_number), callback=self.parse)
        else:
            current_page = 1
        
        links = response.xpath('//a[@class="image pattern"]/@href').getall()
            
        with open(os.path.join(output_dir, cat, child_cat, 'links.txt'), 'a+') as links_file:
            for link in links:
                links_file.write('{}\n'.format(homepage + link))