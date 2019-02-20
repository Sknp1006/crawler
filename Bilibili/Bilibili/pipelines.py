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
        # pwd = os.getcwd()
        # bs_folder = 'bulletscreen\\'
        # com_folder = 'comment\\'
        # self.bs_path = pwd + '\\' + bs_folder
        # self.com_path = pwd + '\\' + com_folder
        # try:
        #     os.mkdir('bulletscreen')
        # except Exception:
        #     pass
        # try:
        #     os.mkdir('comment')
        # except Exception:
        #     pass

    def process_item(self, item, spider):

        # if isinstance(item, BulletScreen):
        #     # return self.process_bs(item)
        #     return item
        # elif isinstance(item, VideoComment):
        #     # return self.process_com(item)
        #     return item
        if isinstance(item, FollowListItem):
            return self.process_fl(item)
        elif isinstance(item, SpaceListItem):
            return self.process_sl(item)
        elif isinstance(item, VideoInfoItem):
            return self.process_vi(item)
        return item

    def process_fl(self, item):
        follower = dict(item)
        try:
            self.fl.write(follower['mid'] + ',' + follower['mid_url'] + ',' + follower['mid_name'] + '\n')
        except Exception as e:
            print("FollowlistPipeline发生错误", e)
        return item

    def process_sl(self, item):
        sl = dict(item)
        try:
            self.sl.write('%s,%s,%s,%s,%s\n' \
                          % (sl['aid'], sl['aid_url'], sl['aid_name'], sl['aid_author'], sl['aid_created']))
        except Exception as e:
            print("SpaceListPipeline发生错误", e)
        return item

    def process_vi(self, item):
        si = dict(item)
        try:
            self.vi.write('%s,%s,%s,%s,%s,%s,%s\n' \
                          % (
                              si['video_cid'], si['video_aid'], si['video_title'], si['video_like'],
                              si['video_coin'], si['video_collection'], si['video_view']))
        except Exception as e:
            print("VideoInfoPipeline发生错误", e)
        return item

    # def process_bs(self, item):
    #     f = open(self.bs_path + item['aid'] + '.csv', 'w', buffering=-1, encoding='utf8')
    #     d = ET.fromstring(item['bullentscreen'])
    #     for i in d:
    #         if i.get('p') is not None:
    #             msg = i.text
    #             attr = i.get('p')
    #             message = {'msg': msg}
    #             f.write(attr + ',' + str(message) + '\n')
    #     f.close()
    #     return item
    #
    # def process_com(self, item):
    #     f = open(self.com_path + item['comment_aid'] + '.csv', 'a', buffering=-1, encoding='utf8')
    #     f.write("1")
    #     f.close()
    #     return item

    def close_spider(self, spider):
        self.fl.close()
        self.sl.close()
        self.vi.close()


class SavePipeline(object):
    def __init__(self):
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

    def process_item(self, item, spider):
        if isinstance(item, BulletScreen):
            return self.process_bs(item)
        elif isinstance(item, VideoComment):
            return self.process_com(item)
        return item

    def process_bs(self, item):
        f = open(self.bs_path + item['aid'] + '.csv', 'w', buffering=-1, encoding='utf8')
        d = ET.fromstring(item['bullentscreen'])
        for i in d:
            if i.get('p') is not None:
                msg = i.text
                attr = i.get('p')
                message = {'msg': msg}
                f.write(attr + ',' + str(message) + '\n')
        f.close()
        return item

    def process_com(self, item):
        f = open(self.com_path + item['comment_aid'] + '.csv', 'a', buffering=-1, encoding='utf8')
        text = json.loads(item['comment_msg'])
        if text['message'] == '0':
            for i in range(20):
                try:
                    mid = text['data']['replies'][i]['member']['mid']
                    uname = text['data']['replies'][i]['member']['uname']
                    sex = text['data']['replies'][i]['member']['sex']
                    message = text['data']['replies'][i]['content']['message']
                    like = text['data']['replies'][i]['like']
                    floor = text['data']['replies'][i]['floor']
                    date = text['data']['replies'][i]['ctime']
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(text['data']['replies'][i]['ctime'])))
                except IndexError:
                    pass
                except Exception as e:
                    print('process_com error', e)
                f.write('{},{},{},{},{},{},{}\n'.format(floor, mid, uname, sex, like, message, date))
        f.close()
        return item


# class FollowlistPipeline(object):
#     def __init__(self):
#         try:
#             self.fl = open('follow_list.csv', 'w', encoding='utf8')
#         except Exception:
#             print('写入文件异常')
#
#     def process_item(self, item, spider):
#         if isinstance(item, FollowListItem):
#             follower = dict(item)
#             try:
#                 self.fl.write(follower['mid'] + ',' + follower['mid_url'] + ',' + follower['mid_name'] + '\n')
#             except Exception as e:
#                 print("FollowlistPipeline发生错误", e)
#         return item
#
#     def close_spider(self, spider):
#         self.fl.close()
#
#
# class SpaceListPipeline(object):
#     def __init__(self):
#         try:
#             self.sl = open('space_list.csv', 'w', encoding='utf8')
#         except Exception:
#             print('写入文件异常')
#
#     def process_item(self, item, spider):
#         if isinstance(item, SpaceListItem):
#             sl = dict(item)
#             try:
#                 self.sl.write('%s,%s,%s,%s,%s\n' \
#                               % (sl['aid'], sl['aid_url'], sl['aid_name'], sl['aid_author'], sl['aid_created']))
#             except Exception as e:
#                 print("SpaceListPipeline发生错误", e)
#         return item
#
#     def close_spider(self, spider):
#         self.sl.close()
#
#
# class VideoInfoPipeline(object):
#     def __init__(self):
#         try:
#             self.vi = open('video_info.csv', 'w', encoding='utf8')
#         except Exception:
#             print('写入文件异常')
#
#     def process_item(self, item, spider):
#         if isinstance(item, VideoInfoItem):
#             si = dict(item)
#             try:
#                 self.vi.write('%s,%s,%s,%s,%s,%s,%s\n' \
#                               % (
#                                   si['video_cid'], si['video_aid'], si['video_title'], si['video_like'],
#                                   si['video_coin'], si['video_collection'], si['video_view']))
#             except Exception as e:
#                 print("VideoInfoPipeline发生错误", e)
#         return item
#
#     def close_spider(self, spider):
#         self.vi.close()
#
#
# # 使用xml.etree.cElementTree
# class BulletScreenPipeline(object):
#     def __init__(self):
#         self.pwd = os.getcwd()
#         self.dir = 'bulletscreen\\'
#         self.dir_path = self.pwd + '\\' + self.dir
#         try:
#             os.mkdir('bulletscreen')
#         except Exception:
#             pass
#
#     def process_item(self, item, spider):
#         if isinstance(item, BulletScreen):
#             f = open(self.dir_path + item['aid'] + '.csv', 'w', buffering=-1, encoding='utf8')
#             d = ET.fromstring(item['bullentscreen'])
#             for i in d:
#                 if i.get('p') is not None:
#                     msg = i.text
#                     attr = i.get('p')
#                     message = {'msg': msg}
#                     f.write(attr + ',' + str(message) + '\n')
#             f.close()
#         return item
#
#
# class CommentPipeline(object):
#     def __init__(self):
#         pwd = os.getcwd()
#         com_folder = 'comment\\'
#         self.com_path = pwd + '\\' + com_folder
#         try:
#             os.mkdir('comment')
#         except Exception:
#             pass
#
#     def process_item(self, item, spider):
#         if isinstance(item, VideoComment):
#             f = open(self.com_path + item['aid'] + '.csv', 'w', buffering=-1, encoding='utf8')
#             f.close()
#         return item
#
#
#
# class SavePipeline(object):
#     def __init__(self):
#         pwd = os.getcwd()
#         bs_folder = 'bulletscreen\\'
#         self.bs_path = pwd + '\\' + bs_folder
#         try:
#             os.mkdir('bulletscreen')
#         except Exception:
#             pass
#         pwd = os.getcwd()
#         com_folder = 'comment\\'
#         self.com_path = pwd + '\\' + com_folder
#         try:
#             os.mkdir('comment')
#         except Exception:
#             pass
#
#     def process_item(self, item, spider):
#         if isinstance(item, BulletScreen):
#             return self.process_bs(item)
#         if isinstance(item, VideoComment):
#             return self.process_com(item)
#         return item
#
#     def process_bs(self, item):
#         f = open(self.bs_path + item['aid'] + '.csv', 'w', buffering=-1, encoding='utf8')
#         d = ET.fromstring(item['bullentscreen'])
#         for i in d:
#             if i.get('p') is not None:
#                 msg = i.text
#                 attr = i.get('p')
#                 message = {'msg': msg}
#                 f.write(attr + ',' + str(message) + '\n')
#         f.close()
#         return item
#
#     def process_com(self, item):
#         f = open(self.com_path + item['aid'] + '.csv', 'w', buffering=-1, encoding='utf8')
#         f.close()
#         return item
