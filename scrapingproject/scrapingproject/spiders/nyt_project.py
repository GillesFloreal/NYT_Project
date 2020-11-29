import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class NytProjectSpider(scrapy.spiders.CrawlSpider):
    name = 'nyt_project'
    allowed_domains = ['www.mo.be']
    start_urls = ['https://www.mo.be/category/thema/milieu/klimaat?page=0']
    rules = [Rule(LinkExtractor(allow=('/category/thema/milieu/klimaat')), follow=True),
             Rule(LinkExtractor(allow=('/nieuws/')), follow=False, callback='parse_article')]


    def parse_article(self, response):
        title = response.xpath('//h1[@class="title"][1]/text()').extract()
        #text = response.xpath("").extract()
        return {'title': title}




#xpath/JSON lines
