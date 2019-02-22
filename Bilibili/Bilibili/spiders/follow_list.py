# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
from math import ceil
from requests import get
from ..items import FollowListItem
from ..items import GetSubmitVideos
from ..items import VideoInfoItem

from ..items import BulletScreen
from ..items import VideoComment


class FollowListSpider(scrapy.Spider):
    name = 'MyBilibili'

    def __init__(self):
        self.usr_mid = '66124873'
        self.cookie = {'buvid3': '20D00332-7A00-4BD3-B5FC-22CDEC541BB081657infoc',
                       ' UM_distinctid': '168e761892733-0d0318551f07ba8-11666e4a-1fa400-168e76189293f',
                       ' LIVE_BUVID': 'AUTO4215500721154664', ' sid': '997kryc7',
                       ' bp_t_offset_66124873': '222961781089934882', ' stardustvideo': '1', ' CURRENT_FNVAL': '16',
                       ' finger': '964b42c0', ' im_notify_type_66124873': '0', ' rpdid': 'psspqpmomdosswsswmiw',
                       ' CURRENT_QUALITY': '74', ' fts': '1550551558', ' DedeUserID': '66124873',
                       ' DedeUserID__ckMd5': '769f4fc4522a775e', ' SESSDATA': 'ac3757d4%2C1553342190%2Ce54c3921',
                       ' bili_jct': 'a088b046752e5f495937bc1db2748593',
                       ' _dfcaptcha': '4c0074e39591cf16656ff5730fb80086'}

        self.start_urls = ["http://api.bilibili.com/x/relation/followings?vmid={usr_mid}&pn={page_num}&ps=20". \
                               format(usr_mid=self.usr_mid, page_num=1)]

    def parse(self, response):
        json_text = response.text
        text = json.loads(json_text)
        # message是字符串类型
        if text['message'] == '0':
            # total是int类型
            total = int(text['data']['total'])
            if int(total) != 0:
                item = FollowListItem()
                for i in range(20):
                    try:
                        mid = str(text['data']['list'][i]['mid'])
                        mid_name = text['data']['list'][i]['uname']
                        mid_url = 'http://space.bilibili.com/{mid_num}/video'.format(mid_num=mid)
                        item['mid'] = mid
                        item['mid_url'] = mid_url
                        item['mid_name'] = mid_name
                    except Exception:
                        break
                    else:
                        yield item
                        start_url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={mid}&pagesize=30&tid=0&page={page_num}'.format(
                            mid=mid, page_num=1)
                        yield scrapy.Request(start_url, callback=self.getSubmitVideos, cookies=self.cookie)

                # 算出总页数以及当前页
                total_page = ceil(total / 20)
                cur_page = re.search(r'pn=(\d+)', response.url).group(1)
                if int(cur_page) < int(total_page):
                    next_urls = "http://api.bilibili.com/x/relation/followings?vmid={usr_mid}&pn={page_num}&ps=20". \
                        format(usr_mid=self.usr_mid, page_num=str(int(cur_page) + 1))  # 返回json字符串
                    yield scrapy.Request(next_urls, callback=self.parse, cookies=self.cookie)  # 到下一页

    def getSubmitVideos(self, response):
        json_text = response.text
        text = json.loads(json_text)
        vlist = text['data']['vlist']
        # 总页数
        total_page = text['data']['pages']
        # 当前页
        cur_page = re.search(r'page=(\d+)', response.url).group(1)
        item = GetSubmitVideos()
        for i in range(30):
            try:
                item['aid'] = str(vlist[i]['aid'])
                item['aid_url'] = 'https://www.bilibili.com/video/av{aid}'.format(aid=item['aid'])
                item['aid_name'] = vlist[i]['title']
                item['aid_author'] = vlist[i]['author']
                item['aid_mid'] = str(vlist[i]['mid'])
                item['aid_length'] = vlist[i]['length']
                item['aid_created'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(vlist[i]['created'])))
                item['aid_description'] = {'description': vlist[i]['description']}
            except Exception:
                break
            else:
                yield item

                start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + item['aid']
                yield scrapy.Request(start_url, callback=self.videoInfos, cookies=self.cookie, meta={'mid': item['aid_mid']})
        # 继续当前UP主的下一页
        if int(cur_page) < int(total_page):
            next_url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={mid}&pagesize=30&tid=0&page={page_num}'.format(
                mid=re.search(r'mid=(\d+)', response.url).group(1), page_num=str(int(cur_page) + 1))
            yield scrapy.Request(next_url, callback=self.getSubmitVideos, cookies=self.cookie)

    def videoInfos(self, response):
        json_text = response.text
        text = json.loads(json_text)
        p_list = []
        item = VideoInfoItem()
        item['mid'] = response.meta['mid']
        item['video_cid'] = str(text['data']['cid'])
        item['video_aid'] = str(text['data']['aid'])
        item['video_title'] = text['data']['title']
        item['video_tname'] = text['data']['tname']
        item['video_like'] = str(text['data']['stat']['like'])
        item['video_coin'] = str(text['data']['stat']['coin'])
        item['video_collection'] = str(text['data']['stat']['favorite'])
        item['video_view'] = str(text['data']['stat']['view'])
        item['video_p'] = str(text['data']['videos'])
        if int(item['video_p']) > 1:
            for i in range(int(item['video_p'])):
                video_ptitle = text['data']['pages'][i]['part']
                video_pcid = str(text['data']['pages'][i]['cid'])
                p_list.append({'pcid': video_pcid, 'ptitle': video_ptitle})
        item['p_list'] = p_list
        yield item



    # 弹幕地址
    # bulletscreen_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=' + item['video_cid']
    # yield scrapy.Request(bulletscreen_url, callback=self.get_bulletscreen, cookies=self.cookie, \
    #                      meta={'aid': item['video_aid']})
    # # 获取弹幕
    # def get_bulletscreen(self, response):
    #     aid = response.meta['aid']
    #     xml_text = response.body
    #     item = BulletScreen()
    #     item['bullentscreen'] = xml_text
    #     item['aid'] = aid
    #     yield item
    #
    # # 获取评论
    # def get_comment(self, response):
    #     json_text = response.text
    #     item = VideoComment()
    #     item['comment_aid'] = response.meta['aid']
    #     item['comments'] = json_text
    #     text = json.loads(json_text)
    #     # 获取下一页
    #     page = text['data']['page']['num']
    #     t_page = text['data']['page']['count']
    #     yield item
    #     if int(page) < int(t_page):
    #         next_url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={page}&type=1&oid={aid}&nohot=1".format(
    #             page=str(int(page) + 1), aid=response.meta['aid'])
    #         yield scrapy.Request(next_url, callback=self.get_comment, cookies=self.cookie,
    #                              meta={'aid': response.meta['aid']})
