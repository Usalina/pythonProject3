import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['www.labirint.ru']
    start_urls = ['https://www.labirint.ru/novelty/',
                  'https://www.labirint.ru/search/%D0%BD%D0%B0%D1%83%D1%87%D0%BD%D0%BE%D0%B5/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//div[@id]/h1/text()").get()
        publisher = response.xpath("//div[@class='publisher']/a[@class='analytics-click-js']/text()").get()
        price_old = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        price_new = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        rating = response.xpath("div[@id='rate']/text()").get()
        url = response.url
        yield BookparserItem(name=name, publisher=publisher, price_old=price_old, price_new=price_new, rating=rating, url=url)
