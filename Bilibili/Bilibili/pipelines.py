# -*- coding: utf-8 -*-
import os
import json
import time
import xml.etree.cElementTree as ET
from .items import FollowListItem
from .items import GetSubmitVideos
from .items import VideoInfoItem
from .items import BulletScreen
from .items import VideoComment


# from multiprocessing import Pool


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class BilibiliPipeline(object):
    def __init__(self):
        try:
            self.fl = open('follow_list.csv', 'w', buffering=1, encoding='utf8')
        except Exception:
            print('写入文件异常')

        # 创建文件夹
        pwd = os.getcwd()
        self.gsv_path = pwd + '\\getSubmitVideos\\'
        self.com_path = pwd + '\\comment\\'
        self.bs_path = pwd + '\\bulletscreen\\'
        self.vi_path = pwd + '\\videoInfos\\'
        try:
            os.mkdir('bulletscreen')
        except Exception:
            pass
        try:
            os.mkdir('comment')
        except Exception:
            pass
        try:
            os.mkdir('getSubmitVideos')
        except Exception:
            pass
        try:
            os.mkdir('videoInfos')
        except Exception:
            pass

    def process_item(self, item, spider):
        if isinstance(item, FollowListItem):
            self.process_fl(item)
        elif isinstance(item, GetSubmitVideos):
            self.process_gsv(item)
        elif isinstance(item, VideoInfoItem):
            self.process_vi(item)
        # elif isinstance(item, BulletScreen):
        #     self.process_bs(item)
        # elif isinstance(item, VideoComment):
        #     self.process_vc(item)
        return item

    # follow_list
    def process_fl(self, item):
        try:
            self.fl.write(item['mid'] + ',' + item['mid_url'] + ',' + item['mid_name'] + '\n')
        except Exception as e:
            print("FollowlistPipeline发生错误", e)

    # getSubmitVideos
    def process_gsv(self, item):
        csv_path = self.gsv_path + item['aid_mid'] + '.csv'
        with open(csv_path, 'a', buffering=1, encoding='utf8') as f:
            f.write('{},{},{},{},{},{},{},{}\n'.format(item['aid'], item['aid_url'], item['aid_name'], item['aid_mid'],
                                                       item['aid_author'], item['aid_length'], item['aid_created'],
                                                       item['aid_description']))

    # videoinfo
    def process_vi(self, item):
        csv_path = self.vi_path + item['mid'] + '.csv'
        with open(csv_path, 'a', buffering=1, encoding='utf8') as f:
            f.write('{},{},{},{},{},{},{},{},{},{}\n'.format(item['video_cid'], item['video_aid'], item['video_title'],
                                                             item['video_tname'], item['video_like'],
                                                             item['video_coin'], item['video_collection'],
                                                             item['video_view'], item['video_p'], item['p_list']))

    # bulletscreen
    # def process_bs(self, item):
    #     with open(self.bs_path + item['aid'] + '.csv', 'w', encoding='utf8') as f:
    #         d = ET.fromstring(item['bullentscreen'])
    #         for i in d:
    #             if i.get('p') is not None:
    #                 msg = i.text
    #                 attr = i.get('p')
    #                 message = {'msg': msg}
    #                 f.write(attr + ',' + str(message) + '\n')
    #
    # # videocomment
    # def process_vc(self, item):
    #     with open(self.com_path + item['comment_aid'] + '.csv', 'a', encoding='utf8') as f:
    #         text = json.loads(item['comments'])
    #         if text['message'] == '0':
    #             for i in range(20):
    #                 try:
    #                     mid = text['data']['replies'][i]['member']['mid']
    #                     uname = text['data']['replies'][i]['member']['uname']
    #                     sex = text['data']['replies'][i]['member']['sex']
    #                     message = {'msg': text['data']['replies'][i]['content']['message']}
    #                     like = text['data']['replies'][i]['like']
    #                     floor = text['data']['replies'][i]['floor']
    #                     date = time.strftime("%Y-%m-%d %H:%M:%S",
    #                                          time.localtime(int(text['data']['replies'][i]['ctime'])))
    #                     device = text['data']['replies'][i]['content']['device']
    #                 except IndexError:
    #                     break
    #                 except Exception:
    #                     break
    #                 else:
    #                     f.write(
    #                         '{},{},{},{},{},{},{},{}\n'.format(floor, mid, uname, sex, device, like, str(message),
    #                                                            date))

    def close_spider(self, spider):
        self.fl.close()
        # self.sl.close()
        # self.vi.close()
        # self.pool.close()
        # self.pool.join()
