# -*- coding: utf-8 -*-
import csv
from .checkpipe import check_spider_pipeline
import sys
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

    @check_spider_pipeline  #判断是否是需要执行的pipeline
    def process_item(self, item, spider):
        follower = dict(item)
        try:
            self.file.write(follower['mid'] + ',' + follower['mid_url'] + ',' + follower['mid_name'] + '\n')
        except Exception as e:
            print("Pipeline发生错误")
        return item

    def open_spider(self, spider):
        print('===================FollowlistPipeline===================')

    def close_spider(self, spider):
        self.file.close()


