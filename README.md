# your-average-cookie
Learning project for data analysis with python

## Start

**First time** create a virtual environment in the `.venv` folder with:

```bash
pyton -m venv .venv
``` 

Activate the venv with

```bash
source .venv/bin/activate
```

Install pacakges in the venv with

```bash
pip install -r requirements.txt
```

You can install new requirements with `pip install [package]` into the venv, then update `requirements.txt` using

```bash
pip freeze > requirements.txt
```

When done, deactivate the venv with the `deactivate` command.

## Scrapy

Part of this project's learning plan is to use scrapy to get data from websites with (cookie) recipes. 

Run scrapy by going into the `cookie-recipes` folder, then using:

```bash
scrapy crawl [name-of-spider]
```

See also the [Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html).

The interactive scrapy shell can be used to explore the content of a page, replacing the url with the page you want:

```bash
scrapy shell "https://quotes.toscrape.com/page/1/"
``` 

