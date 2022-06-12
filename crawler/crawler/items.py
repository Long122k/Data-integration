# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TGDDItem(scrapy.Item):
    images_intro = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    hot_line = scrapy.Field()
    informations = scrapy.Field()
    rating = scrapy.Field()
    link_source = scrapy.Field()
    branch = scrapy.Field()
    type = scrapy.Field()
    # 'Màn hình' = scrapy.Field()
    pass


class DMXItem(scrapy.Item):
    images_intro = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    hot_line = scrapy.Field()
    informations = scrapy.Field()
    rating = scrapy.Field()
    link_source = scrapy.Field()
    branch = scrapy.Field()
    pass
