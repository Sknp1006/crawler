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
    aid_created = scrapy.Field()
    aid_description = scrapy.Field()


class VideoInfoItem(scrapy.Item):
    #视频信息
    video_view = scrapy.Field()  #播放量
    video_like = scrapy.Field()  #点赞
    video_coin = scrapy.Field()  #投币
    video_collection = scrapy.Field()  #收藏
    video_title = scrapy.Field()  #标题
    video_label = scrapy.Field()  #标签
    video_cid = scrapy.Field()  #弹幕地址
    video_aid = scrapy.Field()
    video_reply = scrapy.Field()  #评论数量


class BulletScreen(scrapy.Item):
    message = scrapy.Field()
    aid = scrapy.Field()
    attr = scrapy.Field()


class VideoComment(scrapy.Item):
    pass




