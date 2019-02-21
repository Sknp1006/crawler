# -*- coding: utf-8 -*-
import os
import json
import time
import xml.etree.cElementTree as ET
from .items import FollowListItem
from .items import SpaceListItem
from .items import VideoInfoItem
from .items import BulletScreen
from .items import VideoComment
from multiprocessing import Pool


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
        try:
            self.sl = open('space_list.csv', 'w', buffering=1, encoding='utf8')
        except Exception:
            print('写入文件异常')
        try:
            self.vi = open('video_info.csv', 'w', buffering=1, encoding='utf8')
        except Exception:
            print('写入文件异常')
        pwd = os.getcwd()
        bs_folder = 'bulletscreen\\'
        self.bs_path = pwd + '\\' + bs_folder
        try:
            os.mkdir('bulletscreen')
        except Exception:
            pass
        com_folder = 'comment\\'
        self.com_path = pwd + '\\' + com_folder
        try:
            os.mkdir('comment')
        except Exception:
            pass
        #创建进程池
        # self.pool = Pool()
        # self.pool.apply_async(self.process_item)

    def process_item(self, item, spider):
        if isinstance(item, FollowListItem):
            self.process_fl(item)
        elif isinstance(item, SpaceListItem):
            self.process_sl(item)
        elif isinstance(item, VideoInfoItem):
            self.process_vi(item)
        elif isinstance(item, BulletScreen):
            self.process_bs(item)
        elif isinstance(item, VideoComment):
            self.process_vc(item)
        return item

    # follow_list
    def process_fl(self, item):
        follower = dict(item)
        try:
            self.fl.write(follower['mid'] + ',' + follower['mid_url'] + ',' + follower['mid_name'] + '\n')
        except Exception as e:
            print("FollowlistPipeline发生错误", e)

    # space_list
    def process_sl(self, item):
        sl = dict(item)
        try:
            self.sl.write('%s,%s,%s,%s,%s\n' \
                          % (sl['aid'], sl['aid_url'], sl['aid_name'], sl['aid_author'], sl['aid_created']))
        except Exception as e:
            print("SpaceListPipeline发生错误", e)

    # videoinfo
    def process_vi(self, item):
        si = dict(item)
        try:
            self.vi.write('%s,%s,%s,%s,%s,%s,%s\n' \
                          % (
                              si['video_cid'], si['video_aid'], si['video_title'], si['video_like'],
                              si['video_coin'], si['video_collection'], si['video_view']))
        except Exception as e:
            print("VideoInfoPipeline发生错误", e)

    # bulletscreen
    def process_bs(self, item):
        with open(self.bs_path + item['aid'] + '.csv', 'w', buffering=-1, encoding='utf8') as f:
            d = ET.fromstring(item['bullentscreen'])
            for i in d:
                if i.get('p') is not None:
                    msg = i.text
                    attr = i.get('p')
                    message = {'msg': msg}
                    f.write(attr + ',' + str(message) + '\n')

    # videocomment
    def process_vc(self, item):
        with open(self.com_path + item['comment_aid'] + '.csv', 'a', buffering=-1, encoding='utf8') as f:
            text = json.loads(item['comments'])
            if text['message'] == '0':
                for i in range(20):
                    try:
                        mid = text['data']['replies'][i]['member']['mid']
                        uname = text['data']['replies'][i]['member']['uname']
                        sex = text['data']['replies'][i]['member']['sex']
                        message = {'msg': text['data']['replies'][i]['content']['message']}
                        like = text['data']['replies'][i]['like']
                        floor = text['data']['replies'][i]['floor']
                        date = time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime(int(text['data']['replies'][i]['ctime'])))
                        device = text['data']['replies'][i]['content']['device']
                    except IndexError:
                        break
                    except Exception:
                        break
                    else:
                        f.write(
                            '{},{},{},{},{},{},{},{}\n'.format(floor, mid, uname, sex, device, like, str(message),
                                                               date))

    def close_spider(self, spider):
        self.fl.close()
        self.sl.close()
        self.vi.close()
        # self.pool.close()
        # self.pool.join()