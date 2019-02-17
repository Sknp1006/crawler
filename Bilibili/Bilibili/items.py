# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class followLsitItem(scrapy.Item):
    mid = scrapy.Field()
    mid_url = scrapy.Field()
    mid_name = scrapy.Field()

class upVideoItem(scrapy.Item):
    pass

class videoInfoItem(scrapy.Item):
    pass


