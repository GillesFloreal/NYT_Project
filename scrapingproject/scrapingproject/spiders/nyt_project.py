import scrapy
from scrapy.http import Request


class NytProjectSpider(scrapy.Spider):
    name = 'nyt_project'
    allowed_domains = ['https://www.mo.be/category/thema/milieu/klimaat']
    start_urls = ['https://www.mo.be/category/thema/milieu/klimaat?page=0']

    counter = 0

    def parse_article(self, response):
        text = response.xpath().extract()
        pass

    def parse(self, response):

        links = response.xpath("/response.xpath(/div[@class ='field-items']//a[@class='pointer-link']/@href").extract()
        for link in links:
            yield Request(link, callback=self.parse_article)
        self.counter += 1
        yield Request(f'https://www.mo.be/category/thema/milieu/klimaat?page={self.counter}', callback=self.parse)
        # yield or give the scraped info to scrapy

        pass


#xpath/JSON lines

#f'https://www.mo.be/category/thema/milieu/klimaat?page={counter}'