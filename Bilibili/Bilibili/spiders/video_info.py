# -*- coding: utf-8 -*-
import scrapy
from ..items import videoInfoItem
from ..pipelines import VideoInfoPipelie

class VideoInfoSpider(scrapy.Spider):
    pipeline = set([VideoInfoPipelie, ])
    name = 'video_info'
    allowed_domains = ['bilibili.com']
    start_urls = ['http://bilibili.com/']

    # print(item['mid_url'])
    def parse(self, response):
        pass
