# -*- coding: utf-8 -*-
import scrapy
import csv


class UpVideoSpider(scrapy.Spider):
    name = 'up_video'
    allowed_domains = ['bilibili.com']

    def start_requests(self):
        with open('follow_list.csv', 'r', encoding='utf8') as f:
            data = csv.reader(f)
            print(data)

    def parse(self, response):
        pass
