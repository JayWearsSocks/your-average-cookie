from .parsing import Parsing

import scrapy


def try_or_none(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return None
    return wrapper


class cookieTestSpider(scrapy.Spider):
    name = "cookie_test"

    async def start(self):
        urls = [
            "https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def _clean_number_string(self, input):
        to_remove = str.maketrans('', '', '(),:')
        return input.translate(to_remove)

    def _clean_text_string(self, input):
        to_remove = str.maketrans('', '', ':')
        return input.translate(to_remove).lower().strip()

    def _clean_label_string(self, input):
        return self._clean_text_string(input).replace(' ', '_')

    @try_or_none
    def _parse_recipe_details(self, response):
        recipe_details = response.css(
            'div.mm-recipes-details__content div.mm-recipes-details__item')
        return {
            self._clean_label_string(
                item.css('div.mm-recipes-details__label::text').get()):
            self._clean_text_string(
                item.css('div.mm-recipes-details__value::text').get())
            for item in recipe_details}

    @try_or_none
    def _parse_ingredients(self, response):
        ingredients = response.css(
            '#mm-recipes-structured-ingredients_1-0 ul.mm-recipes-structured-ingredients__list li p')
        return [
            {
                "quantity": i.xpath('.//span[contains(@data-ingredient-quantity, "true")]/text()').get(),
                "unit": i.xpath('.//span[contains(@data-ingredient-unit, "true")]/text()').get(),
                "name": i.xpath('.//span[contains(@data-ingredient-name, "true")]/text()').get(),
            }
            for i in ingredients
        ]

    def parse(self, response):
        yield {
            "test": "test",
            "title": response.css('h1::text').get(),
            "avg_rating":
                Parsing.try_parse_float(
                    response.css(
                        '#mm-recipes-review-bar__rating_1-0::text').get()
            ),
            "num_ratings":
                Parsing.try_parse_int(self._clean_number_string(
                    response.css(
                        '#mm-recipes-review-bar__rating-count_1-0::text').get()
                )),
            "recipe_details": self._parse_recipe_details(response),
            "ingredients": self._parse_ingredients(response),
        }


class CookieSpider(scrapy.Spider):
    name = "cookie"

    # crawl pages from only one page of search results to avoid getting blocked
    async def start(self):
        offset = (int(self.page) - 1) * 24
        self.log(f'Offset is {offset}')
        start_url = f"https://www.allrecipes.com/search?q=cookie&offset={offset}"
        self.log(f'start url is {start_url}')
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        recipes = response.css(
            '#mntl-search-results__list_1-0 a::attr(href)').getall()
        for recipe in recipes:
            recipe_url = response.urljoin(recipe)
            yield scrapy.Request(url=recipe_url, callback=self.parse_recipe, cb_kwargs={'recipe_url': recipe_url})

    def _clean_number_string(self, input):
        to_remove = str.maketrans('', '', '(),:')
        return input.translate(to_remove)

    def _clean_text_string(self, input):
        to_remove = str.maketrans('', '', ':')
        return input.translate(to_remove).lower().strip()

    def _clean_label_string(self, input):
        return self._clean_text_string(input).replace(' ', '_')

    @try_or_none
    def _parse_recipe_details(self, response):
        recipe_details = response.css(
            'div.mm-recipes-details__content div.mm-recipes-details__item')
        return {
            self._clean_label_string(
                item.css('div.mm-recipes-details__label::text').get()):
            self._clean_text_string(
                item.css('div.mm-recipes-details__value::text').get())
            for item in recipe_details}

    @try_or_none
    def _parse_ingredients(self, response):
        ingredients = response.css(
            '#mm-recipes-structured-ingredients_1-0 ul.mm-recipes-structured-ingredients__list li p')
        return [
            {
                "quantity": i.xpath('.//span[contains(@data-ingredient-quantity, "true")]/text()').get(),
                "unit": i.xpath('.//span[contains(@data-ingredient-unit, "true")]/text()').get(),
                "name": i.xpath('.//span[contains(@data-ingredient-name, "true")]/text()').get(),
            }
            for i in ingredients
        ]

    def parse_recipe(self, response, recipe_url=""):
        yield {
            "recipe_url": recipe_url,
            "title": response.css('h1::text').get(),
            "avg_rating":
                Parsing.try_parse_float(
                    response.css(
                        '#mm-recipes-review-bar__rating_1-0::text').get()
            ),
            "num_ratings":
                Parsing.try_parse_int(self._clean_number_string(
                    response.css(
                        '#mm-recipes-review-bar__rating-count_1-0::text').get()
                )),
            "recipe_details": self._parse_recipe_details(response),
            "ingredients": self._parse_ingredients(response),
        }
