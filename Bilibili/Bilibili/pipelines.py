# -*- coding: utf-8 -*-
import os
import xml.etree.cElementTree as ET
from .items import FollowListItem
from .items import SpaceListItem
from .items import VideoInfoItem
from .items import BulletScreen
from multiprocessing import Pool


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BilibiliPipeline(object):
    def process_item(self, item, spider):
        return item


class FollowlistPipeline(object):
    def __init__(self):
        try:
            self.file = open('follow_list.csv', 'w', encoding='utf8')
        except Exception:
            print('写入文件异常')

    # @check_spider_pipeline  #判断是否是需要执行的pipeline
    def process_item(self, item, spider):
        if isinstance(item, FollowListItem):
            follower = dict(item)
            try:
                self.file.write(follower['mid'] + ',' + follower['mid_url'] + ',' + follower['mid_name'] + '\n')
            except Exception as e:
                print("FollowlistPipeline发生错误", e)
        return item

    def open_spider(self, spider):
        print('===================FollowlistPipeline===================')

    def close_spider(self, spider):
        self.file.close()


class SpaceListPipeline(object):
    def __init__(self):
        try:
            self.file = open('space_list.csv', 'w', encoding='utf8')
        except Exception:
            print('写入文件异常')

    # @check_spider_pipeline  #判断是否是需要执行的pipeline
    def process_item(self, item, spider):
        if isinstance(item, SpaceListItem):
            sl = dict(item)
            try:
                self.file.write('%s,%s,%s,%s,%s\n' \
                                % (sl['aid'], sl['aid_url'], sl['aid_name'], sl['aid_author'], sl['aid_created']))
            except Exception as e:
                print("SpaceListPipeline发生错误", e)
        return item

    def open_spider(self, spider):
        print('===================SpacelistPipeline===================')

    def close_spider(self, spider):
        self.file.close()


class VideoInfoPipeline(object):
    def __init__(self):
        try:
            self.file = open('video_info.csv', 'w', encoding='utf8')
        except Exception:
            print('写入文件异常')

    def process_item(self, item, spider):
        if isinstance(item, VideoInfoItem):
            si = dict(item)
            try:
                self.file.write('%s,%s,%s,%s,%s,%s,%s\n' \
                                % (
                                    si['video_cid'], si['video_aid'], si['video_title'], si['video_like'],
                                    si['video_coin'],
                                    si['video_collection'], si['video_view']))
            except Exception as e:
                print("VideoInfoPipeline发生错误", e)
        return item

    def open_spider(self, spider):
        print('===================VideoInfoPipelinePipeline===================')

    def close_spider(self, spider):
        self.file.close()


#使用lxml解析的方法
# class BulletScreenPipeline(object):
#     def __init__(self):
#         self.pwd = os.getcwd()
#         self.dir = 'bulletscreen\\'
#         self.dir_path = self.pwd + '\\' + self.dir
#         try:
#             os.mkdir('bulletscreen')
#         except Exception:
#             pass
#         # self.t = Thread(target=self.process_item)
#         # self.t.start()
#         self.t = Pool()
#         self.t.apply_async(self.process_item)
#
#     def process_item(self, item, spider):
#         if isinstance(item, BulletScreen):
#             f = open(self.dir_path + item['aid'] + '.csv', 'w', buffering=-1, encoding='utf8')
#             i = 7
#             while True:
#                 try:
#                     d = etree.fromstring(item['bullentscreen'])[i]
#                 except Exception:
#                     break
#                 msg = d.text
#                 attr = d.attrib['p']
#                 message = {'msg': msg}
#                 f.write(attr + ',' + str(message) + '\n')
#                 i += 1
#             f.close()
#         return item
#
#     def close_spider(self, spider):
#         self.t.close()
#         self.t.join()


#使用xml.etree.cElementTree
class BulletScreenPipeline(object):
    def __init__(self):
        self.pwd = os.getcwd()
        self.dir = 'bulletscreen\\'
        self.dir_path = self.pwd + '\\' + self.dir
        try:
            os.mkdir('bulletscreen')
        except Exception:
            pass
        self.t = Pool()
        self.t.apply_async(self.process_item)

    def process_item(self, item, spider):
        if isinstance(item, BulletScreen):
            f = open(self.dir_path + item['aid'] + '.csv', 'w', buffering=-1, encoding='utf8')
            d = ET.fromstring(item['bullentscreen'])
            for i in d:
                if i.get('p') is not None:
                    msg = i.text
                    attr = i.get('p')
                    message = {'msg': msg}
                    f.write(attr + ',' + str(message) + '\n')
            f.close()
        return item

    def close_spider(self, spider):
        self.t.close()
        self.t.join()