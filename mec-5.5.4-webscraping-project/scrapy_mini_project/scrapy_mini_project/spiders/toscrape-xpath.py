import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.xpath("descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]"):
            yield {
                'text': quote.xpath("descendant-or-self::span[@class and contains(concat(' ', normalize-space(@class), ' '), ' text ')]/text()").get(),
                'author': quote.xpath("span/small/text()").get(),
                'tags': quote.xpath("descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' tags ')]/descendant-or-self::*/a[@class and contains(concat(' ', normalize-space(@class), ' '), ' tag ')]/text()").getall()
            }

        next_page = response.xpath(
            "descendant-or-self::li[@class and contains(concat(' ', normalize-space(@class), ' '), ' next ')]/descendant-or-self::*/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
