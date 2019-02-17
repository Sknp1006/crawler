# -*- coding: utf-8 -*-
import scrapy
import json
import re
from math import ceil
from requests import get
from ..items import FollowListItem
from ..items import SpaceListItem
from ..items import VideoInfoItem
from ..pipelines import FollowlistPipeline

class FollowListSpider(scrapy.Spider):
    name = 'follow_list'
    pipeline = set([FollowlistPipeline, ])
    usr_mid = '66124873'
    # start_urls = ['http://bilibili.com/']
    cookie = {'_uuid': 'DA5FB876-B0DA-A08A-B5A6-3B53F11593B778782infoc', ' LIVE_BUVID': 'AUTO7515472104257092', ' sid': 'l1x674fb', ' fts': '1547267994', ' CURRENT_FNVAL': '16', ' rpdid': 'oqqspoqqpsdospmixqwww', ' stardustvideo': '1', ' UM_distinctid': '168473ea13a5b6-0be1ff6de870f7-3257487f-1fa400-168473ea13bb51', ' finger': 'edc6ecda', ' im_notify_type_66124873': '0', ' DedeUserID': '66124873', ' DedeUserID__ckMd5': '769f4fc4522a775e', ' SESSDATA': 'df5b8e46%2C1550480697%2C4a641311', ' bili_jct': '7913bf65326b9d976ae0d55ec8980054', ' buvid3': '04295C13-CC6E-443F-B86A-1403CCE0386D84602infoc', ' pgv_pvi': '1684714496', ' CURRENT_QUALITY': '112', ' bp_t_offset_66124873': '221318921734487900', ' _dfcaptcha': '057f8907f688ec54653cb21270f1e712'}
    cookie = {'_uuid': 'DA5FB876-B0DA-A08A-B5A6-3B53F11593B778782infoc', ' LIVE_BUVID': 'AUTO7515472104257092', ' sid': 'l1x674fb', ' fts': '1547267994', ' CURRENT_FNVAL': '16', ' rpdid': 'oqqspoqqpsdospmixqwww', ' stardustvideo': '1', ' UM_distinctid': '168473ea13a5b6-0be1ff6de870f7-3257487f-1fa400-168473ea13bb51', ' im_notify_type_66124873': '0', ' buvid3': '04295C13-CC6E-443F-B86A-1403CCE0386D84602infoc', ' pgv_pvi': '1684714496', ' CURRENT_QUALITY': '112', ' bp_t_offset_66124873': '221318921734487900', ' DedeUserID': '66124873', ' DedeUserID__ckMd5': '769f4fc4522a775e', ' SESSDATA': '5d38cac3%2C1552982279%2Ca20ae521', ' bili_jct': '2cd2e645ba0065b2e3b6ea6c158c4bf5', ' _dfcaptcha': 'b2c5e0ecab9cdbc0ab3881a27a0616fd'}
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
        item = FollowListItem()
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
            except KeyError:
                pass
            else:
                yield item
    #         start_url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={mid}&pagesize=30&tid=0&page=1'.format(mid=item['mid'])
    #         yield scrapy.Request(start_url, callback=self.second_process, cookies=self.cookie)
    #
    # #控制页数
    # def second_process(self, response):
    #     json_text = response.text
    #     text = json.loads(json_text)
    #     page = text['data']['pages']
    #     pattern = re.compile(r'\d+$')
    #     for i in range(1, page+1):
    #         next_url = re.sub(pattern, str(i), response.url)
    #         yield scrapy.Request(next_url, callback=self.space_list, cookies=self.cookie)
    #
    # #提取数据
    # def space_list(self, response):
    #     json_text = response.text
    #     text = json.loads(json_text)
    #     vlist = text['data']['vlist']
    #     count = text['data']['count']
    #     item = BilibiliItem()
    #     for i in range(30):
    #         try:
    #             item['aid'] = str(vlist[i]['aid'])
    #             item['aid_url'] = 'https://www.bilibili.com/video/av{aid}'.format(aid=item['aid'])
    #             item['aid_name'] = vlist[i]['title']
    #             item['aid_count'] = count
    #             item['aid_author'] = vlist[i]['author']
    #         except IndexError:
    #             pass
    #         except KeyError:
    #             pass
    #         except Exception:
    #             pass
    #         else:
    #             yield item