from pathlib import Path
from .parsing import Parsing

import scrapy

class cookieTestSpider(scrapy.Spider):
    name = "cookie_test"

    async def start(self):
        urls = [
            "https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def _clean_string(self, input):
        to_remove = str.maketrans('', '', '(),')
        return input.translate(to_remove)

    def parse(self, response):
        self.log('DEBUG: parsing recipe')
        yield {
            "test": "test",
            "title": response.css('h1::text').get(),
            "avg_rating": Parsing.try_parse_float(response.css('#mm-recipes-review-bar__rating_1-0::text').get()),
            "num_ratings": Parsing.try_parse_int(self._clean_string(response.css('#mm-recipes-review-bar__rating-count_1-0::text').get()))        
        }
        self.log('DEBUG: done parsing recipe')


class CookieSpider(scrapy.Spider):
    name = "cookie"

    async def start(self):
        urls = [
            "https://www.allrecipes.com/search?q=cookie",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        recipes = response.css('#mntl-search-results__list_1-0 a::attr(href)').getall()
        for recipe in recipes:
            recipe_url = response.urljoin(recipe)
            yield scrapy.Request(url=recipe_url, callback=self.parse_recipe, cb_kwargs={'recipe_url': recipe_url})

        next_page = response.css('li.mntl-pagination__next a::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def _clean_string(self, input):
        to_remove = str.maketrans('', '', '(),')
        return input.translate(to_remove)

    def parse_recipe(self, response, recipe_url=""):
        yield {
            "recipe_url": recipe_url,
            "title": response.css('h1::text').get(),
            "avg_rating": Parsing.try_parse_float(response.css('#mm-recipes-review-bar__rating_1-0::text').get()),
            "num_ratings": Parsing.try_parse_int(self._clean_string(response.css('#mm-recipes-review-bar__rating-count_1-0::text').get()))        
        }
