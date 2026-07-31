import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    async def start(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quotes = response.css(".quote")
        for quote in quotes:
            yield {
                "text": quote.css(".text::text").get(),
                "author": quote.css(".author::text").get(),
                "tags": quote.css(".tags a.tag::text").getall(),
            }

        next_page = response.css(".pager .next a").xpath("@href").get()
        if next_page is not None:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
