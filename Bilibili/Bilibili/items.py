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
    mid_url = scrapy.Field()

    aid = scrapy.Field()
    aid_url = scrapy.Field()
    aid_name = scrapy.Field()

class videoInfoItem(scrapy.Item):
    video_like = scrapy.Field()
    video_coin = scrapy.Field()
    video_collection = scrapy.Field()
    video_title = scrapy.Field()
    video_label = scrapy.Field()

    bullet_screen = scrapy.Field()
    video_comment = scrapy.Field()


