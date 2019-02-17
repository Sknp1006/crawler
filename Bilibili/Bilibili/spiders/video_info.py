# -*- coding: utf-8 -*-
import scrapy


class VideoInfoSpider(scrapy.Spider):
    name = 'video_info'
    allowed_domains = ['bilibili.com']
    start_urls = ['http://bilibili.com/']

    def parse(self, response):
        pass
