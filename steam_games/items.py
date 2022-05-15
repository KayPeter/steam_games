# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamGamesItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    title = scrapy.Field()
    release_date = scrapy.Field()
    discount_rate = scrapy.Field()
    discount_price = scrapy.Field()
    original_price = scrapy.Field()
    pass
