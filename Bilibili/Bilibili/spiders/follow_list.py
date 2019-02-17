# -*- coding: utf-8 -*-
import scrapy
import json
from math import ceil
from requests import get
from ..items import followLsitItem
from ..pipelines import FollowlistPipeline

class FollowListSpider(scrapy.Spider):
    pipeline = set([FollowlistPipeline, ])
    name = 'follow_list'
    usr_mid = '66124873'
    allowed_domains = ['bilibili.com']
    # start_urls = ['http://bilibili.com/']
    cookie = {'_uuid': 'F8A866BC-1943-4CE9-4A31-932E5547B6CD24769infoc',
              ' buvid3': '356B65DB-7618-4FC3-BBBD-780D03868DF384624infoc', ' LIVE_BUVID': 'AUTO2515499735515018',
              ' stardustvideo': '1', ' CURRENT_FNVAL': '16', ' rpdid': 'psspqpmowdospllmmqpw', ' sid': 'c5kkso2g',
              ' UM_distinctid': '168e9901b0986a-0bb783c240b5b9-b781636-1fa400-168e9901b0a50a', ' fts': '1550106948',
              ' DedeUserID': '66124873', ' DedeUserID__ckMd5': '769f4fc4522a775e',
              ' SESSDATA': '70c078a8%2C1552700797%2Cdce86c21', ' bili_jct': '9fac6bbb3ea0d46fa8cad51c3a53ce66',
              ' bp_t_offset_66124873': '220275811618468531'}
    total_page = 0
    page = 0

    def start_requests(self):
        get_page = get("http://api.bilibili.com/x/relation/followings?vmid={usr_mid}&pn={page_num}&ps=20".\
                    format(usr_mid=self.usr_mid, page_num=1))
        total_page = int(json.loads(get_page.text)['data']['total'])  #计算页数
        if total_page == 0:
            pass
        else:
            page = ceil(total_page/20)
            for i in range(1, page+1):
                start_urls = "http://api.bilibili.com/x/relation/followings?vmid={usr_mid}&pn={page_num}&ps=20".\
                        format(usr_mid=self.usr_mid, page_num=i)  #返回json字符串
                yield scrapy.Request(start_urls, callback=self.parse, cookies=self.cookie)  #到下一页

    def parse(self, response):
        json_text = response.text
        text = json.loads(json_text)
        # 创建Item对象
        item = followLsitItem()
        for i in range(20):
            try:
                mid = str(text['data']['list'][i]['mid'])
                mid_name = text['data']['list'][i]['uname']
                mid_url = 'http://space.bilibili.com/{mid_num}/video'.format(mid_num=mid)
                item['mid'] = mid
                item['mid_url'] = mid_url
                item['mid_name'] = mid_name
            except IndexError:
                pass
            # print(mid, mid_name, mid_url)
            yield item
