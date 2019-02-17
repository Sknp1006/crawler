# -*- coding: utf-8 -*-
import scrapy
import csv
from ..items import upVideoItem
from ..pipelines import UpVideoPipeline


class UpVideoSpider(scrapy.Spider):
    pipeline = set([UpVideoPipeline, ])
    name = 'up_video'
    allowed_domains = ['bilibili.com']
    cookie = {'_uuid': 'F8A866BC-1943-4CE9-4A31-932E5547B6CD24769infoc',
              ' buvid3': '356B65DB-7618-4FC3-BBBD-780D03868DF384624infoc', ' LIVE_BUVID': 'AUTO2515499735515018',
              ' stardustvideo': '1', ' CURRENT_FNVAL': '16', ' rpdid': 'psspqpmowdospllmmqpw', ' sid': 'c5kkso2g',
              ' UM_distinctid': '168e9901b0986a-0bb783c240b5b9-b781636-1fa400-168e9901b0a50a', ' fts': '1550106948',
              ' DedeUserID': '66124873', ' DedeUserID__ckMd5': '769f4fc4522a775e',
              ' SESSDATA': '70c078a8%2C1552700797%2Cdce86c21', ' bili_jct': '9fac6bbb3ea0d46fa8cad51c3a53ce66',
              ' bp_t_offset_66124873': '220275811618468531'}

    # def start_requests(self):
    #     print('====================请求pipe==================')
    #     item = upVideoItem()
    #     yield item
    # https://space.bilibili.com/ajax/member/getSubmitVideos?mid=324753357&pagesize=30&tid=0&page=2
    def start_requests(self):
        with open('follow_list.csv', 'r', encoding='utf8') as f:
            rows = csv.reader(f)
            for row in rows:
                mid_url = row[1]
                start_url = mid_url + '?tid=0&page=1'
                yield scrapy.Request(start_url, callback=self.parse, cookies=self.cookie)
        #传入的url
        # http://space.bilibili.com/206840230/video
        #目标url
        #https://space.bilibili.com/324753357/video?tid=0&page=2

    def parse(self, response):
        print(response.text)