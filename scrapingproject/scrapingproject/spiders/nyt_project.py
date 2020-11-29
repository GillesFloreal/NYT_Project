import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class NytProjectSpider(scrapy.spiders.CrawlSpider):
    name = 'nyt_project'
    allowed_domains = ['www.mo.be']
    start_urls = ['https://www.mo.be/category/thema/milieu/klimaat?page=0']
    rules = [Rule(LinkExtractor(allow=('/category/thema/milieu/klimaat')), follow=True),
             Rule(LinkExtractor(allow=('/nieuws/', '/opinie/', '/analyse/', '/boek/', '/commentaar/', '/interview/',
             '/beeld/', 'zeronaut/', '/column/', '/essay/', '/wereldblog/', )), follow=False, callback='parse_article')]


    def parse_article(self, response):
        title = response.xpath('//h1[@class="title"][1]/text()').extract()
        #header = response.xpath('//div[@class=""]/text()').extract()
        #subtitles = response.xpath('//div[contains(@property, 'schema:articleBody')]/h2/text()').extract()

        # the date and author are separated with a '.', so we can extract them with the .split() function
        #date_and_author = response.xpath('//span[@property="dc:date dc:created"]').extract()
        #date_and_author_split = date_and_author.split('.')
        #author = date_and_author_split[0]
        #date = date_and_author_split[1]

        body = response.xpath('//div[contains(@property, "schema:articleBody")]//p').extract()

        # to extract the article type we can simply look in the url
        article_url = response.request.url
        article_url_removed = article_url.replace("https://", "")
        article_url_split = article_url_removed.split('/')
        article_type = article_url_split[1]         # because of how the url is, the article type will always be there

        return {'title': title, 'body': body, 'article_type': article_type}




#xpath/JSON lines
