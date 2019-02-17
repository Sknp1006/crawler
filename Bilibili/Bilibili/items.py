# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    pass

class FollowListItem(scrapy.Item):
    #关注列表
    mid = scrapy.Field()
    mid_url = scrapy.Field()
    mid_name = scrapy.Field()

class SpaceListItem(scrapy.Item):
    #up主空间
    aid = scrapy.Field()
    aid_url = scrapy.Field()
    aid_name = scrapy.Field()
    aid_count = scrapy.Field()
    aid_author = scrapy.Field()
    fans_count = scrapy.Field()

class VideoInfoItem(scrapy.Item):
    #视频信息
    video_like = scrapy.Field()
    video_coin = scrapy.Field()
    video_collection = scrapy.Field()
    video_title = scrapy.Field()
    video_label = scrapy.Field()

    bullet_screen = scrapy.Field()
    video_comment = scrapy.Field()


