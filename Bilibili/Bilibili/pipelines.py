# -*- coding: utf-8 -*-
import csv
from .checkpipe import check_spider_pipeline
from .items import FollowListItem
from .items import SpaceListItem
from .items import VideoInfoItem
from .items import BulletScreen
from .items import VideoComment
import sys
import os


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
                % (si['video_cid'], si['video_aid'], si['video_title'], si['video_like'], si['video_coin'], si['video_collection'], si['video_view']))
            except Exception as e:
                print("VideoInfoPipeline发生错误", e)
        return item

    def open_spider(self, spider):
        print('===================VideoInfoPipelinePipeline===================')

    def close_spider(self, spider):
        self.file.close()


class BulletScreenPipeline(object):
    def __init__(self):
        self.pwd = os.getcwd()
        self.dir = 'bulletscreen\\'
        self.dir_path = self.pwd + '\\' + self.dir
        try:
            os.mkdir('bulletscreen')
        except Exception:
            pass

    def process_item(self, item, spider):
        if isinstance(item, BulletScreen):
            self.f = open(self.dir_path + item['aid'] + '.csv', 'a', encoding='utf8')
            message = {'msg': item['message']}
            attr = item['attr']
            self.f.write(attr + ',' + str(message) + '\n')

    def close_spider(self, spider):
        self.f.close()

class VideoCommentpipeline(object):
    pass
