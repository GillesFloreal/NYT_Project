import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from inscriptis import get_text
import re


class NytProjectSpider(scrapy.spiders.CrawlSpider):
    name = 'nyt_project'
    allowed_domains = ['www.mo.be']
    start_urls = ['https://www.mo.be/category/thema/milieu/klimaat?page=0']
    rules = [Rule(LinkExtractor(allow=('/category/thema/milieu/klimaat')), follow=True),
             Rule(LinkExtractor(allow=('/nieuws/', '/opinie/', '/analyse/', '/boek/', '/commentaar/', '/interview/',
             '/beeld/', 'zeronaut/', '/column/', '/essay/', '/wereldblog/', '/reportage/')),
             follow=False, callback='parse_article')]

    def parse_article(self, response):
        title = response.xpath('//h1[@class="title"][1]/text()').extract()
        header = response.xpath('//div[@class="title-wrapper"]/div/div/div/text()').extract()

        try:  # sometimes articles don't have headers
            header_string = header[0]
        except:
            header_string = ""

        date = response.xpath('//span[contains(@property, "dc:date")]/text()').extract()
        # in order to extract the date cleanly, some operations have to be done before exporting
        try:
            date_string = date[1]
            date_string_no_space = date_string[1::]
        except:  # rarely, the date will be formatted in another way
            date_string_no_space = date[0]
        author = response.xpath('//span[contains(@property, "dc:date")]/em').extract()

        # the property schema:articleBody encapsulates the whole article, this avoids the problem of unwanted text
        # sometimes <div> classes are inside of the <p> classes. These divs are unwanted so have to be deselected
        # these carry no article content
        body = response.xpath('//div[contains(@property, "schema:articleBody")]'
                              '/p[not(descendant-or-self::div)]').extract()
        subtitles_direct_children = response.xpath('//div[contains(@property, "schema:articleBody")]'
                                                   '/h2/text()').extract()
        try:
            subtitles_descendant_children = response.xpath('//div[contains(@property, "schema:articleBody")]'
                                                           '/h2/descendant-or-self::span[not(@class, "field-content")]'
                                                           '/text()').extract()
        except:
            subtitles_descendant_children = []

        subtitles = subtitles_direct_children + subtitles_descendant_children

        # to extract the article type, the url can be used
        article_url = response.request.url
        article_url_removed = article_url.replace("https://", "")
        article_url_split = article_url_removed.split('/')
        article_type = article_url_split[1]         # because of how the url is, the article type will always be there

        return {'title': title[0], 'header': header_string, 'subtitles': subtitles,
                'date': date_string_no_space, 'author': self.clean_html(author), 'article_type': article_type,
                'url': article_url, 'body': self.clean_html(body) }

    def clean_html(self, html_list):

        html_string_clean = ""
        for html_item in html_list:
            html_item_clean = get_text(html_item)  # This removes all html-elements from the text
            pattern = re.compile('(?<=\\n[A-Z]) (?=[A-z])')  # RegEx to remove spaces caused by letrines (eg D aar)
            html_string_clean += pattern.sub("", html_item_clean)

        return html_string_clean


