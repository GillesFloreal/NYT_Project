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

        try:
            header_string = header[0]
        except:
            header_string = header

        date = response.xpath('//span[contains(@property, "dc:date")]/text()').extract()
        author = response.xpath('//span[contains(@property, "dc:date")]/em').extract()

        # the property schema:articleBody encapsulates the whole article, this avoids the problem of unwanted text
        # sometimes <div> classes are inside of the <p> classes. These div's were unwanted so have to be deselected
        body = response.xpath('//div[contains(@property, "schema:articleBody")]'
                              '/p[not(descendant-or-self::div)]').extract()
        subtitles = response.xpath('//div[contains(@property, "schema:articleBody")]'
                                   '/h2').extract()

        # to extract the article type, the url can be used
        article_url = response.request.url
        article_url_removed = article_url.replace("https://", "")
        article_url_split = article_url_removed.split('/')
        article_type = article_url_split[1]         # because of how the url is, the article type will always be there

        # in order to extract the date cleanly, some operations have to be done before exporting
        date_string = date[1]
        date_string_no_space = date_string[1::]

        return {'title': title[0], 'body': self.clean_html(body), 'article_type': article_type,
                'date': date_string_no_space, 'author': self.clean_html(author), 'header': header_string,
                'subtitles': self.clean_html_subtitles(subtitles), 'url': article_url}

    def clean_html(self, html_list):

        html_string_clean = ""
        for html_item in html_list:
            html_item_clean = get_text(html_item)  # This removes all html-elements from the text
            pattern = re.compile('(?<=\\n[A-Z]) (?=[A-z])')  # RegEx to remove text errors caused by letrines (eg D aar)
            html_string_clean += pattern.sub("", html_item_clean)

        return html_string_clean

    def clean_html_subtitles(self, subtitles_list):
        html_list_clean = []
        for html_item in subtitles_list:
            html_item_clean = get_text(html_item)
            html_item_cleaned = html_item_clean.replace(
                "\n      Blijf op de hoogte\n\n            Schrijf je in op onze nieuwsbrieven en blijf op de hoogte van het mondiale nieuws\n              eMO*: 2 keer per week het beste MO* Daily: Dagelijkse toppers Ik ga akkoord met het privacybeleid *\n                Anti-spam code:",
                "")
            # the above operation is necessary to correct small mishaps that creep into the html code,
            # the message will always be the same, thus it is a small tweak
            html_item_cleaned_again = html_item_cleaned.replace("\n", "")
            html_list_clean.append(html_item_cleaned_again)

        return html_list_clean

