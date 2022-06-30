import scrapy
import os

class PngImgSpider(scrapy.Spider):
    name = "pngimg"
    

    def start_requests(self):
        urls = [line.strip() for line in open('/mnt/c/Users/QuangND/data/1019_crawl_img/crawl_images/pngimg/child_links.txt', 'r')]
        for url in urls:
            cat = url.strip().split('/')[-3]
            child_cat = url.strip().split('/')[-2]
            if os.path.exists(os.path.join('/mnt/c/Users/QuangND/data/1019_crawl_img/crawl_images/pngimg', cat, child_cat, 'links.txt')):
                pass
                #print('Skip category {} child catergory {}'.format(cat, child_cat))
            else:
                #print('Crawl {}'.format(url))
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        homepage = 'http://pngimg.com'
        output_dir = '/mnt/c/Users/QuangND/data/1019_crawl_img/crawl_images/pngimg'
        url = response.request.url
#         if 'ip' in url:
#             print(respone.getall())
        cat = url.split('/')[-3]
        child_cat = url.split('/')[-2]
        print(cat, child_cat)
        links = response.xpath('//div[@class="png_png png_imgs"]/a/noscript/img/@src').getall()
        
        if not os.path.exists(os.path.join(output_dir, cat)):
            os.mkdir(os.path.join(output_dir, cat))
        if not os.path.exists(os.path.join(output_dir, cat, child_cat)):
            os.mkdir(os.path.join(output_dir, cat, child_cat))
            
        with open(os.path.join(output_dir, cat, child_cat, 'links.txt'), 'w') as links_file:
            for link in links:
                links_file.write('{}\n'.format(homepage + link))