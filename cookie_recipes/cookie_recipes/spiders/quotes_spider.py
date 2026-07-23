from pathlib import Path

import scrapy

# from .data_organization import DataOrganization

DATADIR = Path("webdata")

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # datadir = DataOrganization.create_data_directory(name)

    async def start(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # self.datadir.joinpath(Path(f"quotes-{page}.html")).write_bytes(response.body)
        # self.log(f"Saved page {page}")

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