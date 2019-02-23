# -*- coding: utf-8 -*-
import os
import time
import pandas as pd
import xml.etree.cElementTree as ET
from .items import FollowListItem
from .items import GetSubmitVideos
from .items import VideoInfoItem
from .items import BulletScreen
from .items import VideoComment

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class BilibiliPipeline(object):
    def __init__(self):
        # 创建文件夹
        pwd = os.getcwd()
        self.gsv_path = pwd + '\\getSubmitVideos\\'
        self.com_path = pwd + '\\comments\\'
        self.bs_path = pwd + '\\bulletScreen\\'
        self.vi_path = pwd + '\\videoInfos\\'
        try:
            os.mkdir('bulletscreen')
        except Exception:
            pass
        try:
            os.mkdir('comments')
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
        elif isinstance(item, BulletScreen):
            self.process_bs(item)
        elif isinstance(item, VideoComment):
            self.process_vc(item)
        return item

    # follow_list
    def process_fl(self, item):
        with open('follow_list.csv', 'a', encoding='utf8') as f:
            mid = str(item['mid'])
            mid_url = item['mid_url']
            mid_name = item['mid_name']
            f.write('{},{},{}\n'.format(mid, mid_url, mid_name))

    # getSubmitVideos
    def process_gsv(self, item):
        mid = str(item['aid_mid'][0])
        csv_path = self.gsv_path + 'mid' + mid + '.csv'

        aid = pd.Series(item['aid'])
        aid_name = pd.Series(item['aid_name'])
        aid_author = pd.Series(item['aid_author'])
        aid_mid = pd.Series(item['aid_mid'])
        aid_length = pd.Series(item['aid_length'])
        aid_created = pd.Series(item['aid_created'])
        aid_description = pd.Series(item['aid_description'])

        con = pd.concat([aid, aid_name, aid_mid, aid_author, aid_length, aid_created, aid_description], axis=1)
        con.to_csv(csv_path, mode='a', index=False, header=0)

    # videoinfo
    def process_vi(self, item):
        mid = str(item['mid'])
        csv_path = self.vi_path + 'mid' + mid + '.csv'
        with open(csv_path, 'a', encoding='utf8') as f:
            f.write('{},{},{},{},{},{},{},{},{},{}\n'.format(item['video_cid'], item['video_aid'], item['video_title'],
                                                             item['video_tname'], item['video_like'],
                                                             item['video_coin'], item['video_collection'],
                                                             item['video_view'], item['video_p'], str(item['p_list'])))

    # bulletscreen
    def process_bs(self, item):
        csv_path = self.bs_path + 'aid' + item['aid'] + '.csv'
        attr = pd.Series(item['attr'])
        msg = pd.Series(item['msg'])

        con = pd.concat([attr, msg], axis=1)
        con.to_csv(csv_path, mode='a', index=False, header=0)

    # # videocomment
    def process_vc(self, item):
        aid = str(item['com_aid'])
        csv_path = self.com_path + 'aid' + aid + '.csv'
        # com_aid = pd.Series(item['com_aid'])
        com_mid = pd.Series(item['com_mid'])
        com_uname = pd.Series(item['com_uname'])
        com_sex = pd.Series(item['com_sex'])
        com_message = pd.Series(item['com_message'])
        com_like = pd.Series(item['com_like'])
        com_floor = pd.Series(item['com_floor'])
        com_date = pd.Series(item['com_date'])
        com_device = pd.Series(item['com_device'])

        con = pd.concat([com_floor, com_mid, com_uname, com_sex, com_device, com_like, com_message, com_date], axis=1)
        con.to_csv(csv_path, mode='a', index=False, header=0)
