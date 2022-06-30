import scrapy
import pandas as pd

class MetaInfoSpider(scrapy.Spider):
    name = "meta_info"
    df = pd.read_csv('38k_links.csv')
    url = df.loc[1:5,"HOMEPAGE_URL"]
    list_urls = url.to_list()
    print(list_urls) 

    def start_requests(self):
        # urls = [
        #     'http://1080lab.com/'
        # ]
        df = pd.read_csv('38k_links.csv')
        url = df.loc[1:5,"HOMEPAGE_URL"]
        list_urls = url.to_list()
        urls = list_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'meta_info-{page}.html'

        link = response.xpath('//meta[@name="Description"]/@content').getall()
        # link = response.xpath('//title/tetxt()').get()

        with open(filename, 'w', encoding = "utf-8") as f:
            # f.write(response.body)
            for i in range(0,len(link)):
                f.write(page + ": " + str(link[i] + "\n"))
        self.log(f'Saved file {filename}')