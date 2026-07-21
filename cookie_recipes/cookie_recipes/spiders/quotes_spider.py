from pathlib import Path

import scrapy

from .data_organization import DataOrganization

DATADIR = Path("webdata")

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    datadir = DataOrganization.create_data_directory(name)

    async def start(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        self.datadir.joinpath(Path(f"quotes-{page}.html")).write_bytes(response.body)
        self.log(f"Saved page {page}")