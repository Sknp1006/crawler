# -*- coding: utf-8 -*-

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
            print('文件异常')

    def process_item(self, item, follow_list):
        follower = dict(item)
        try:
            self.file.write(follower['mid'] + ',' + follower['mid_url'] + ',' + follower['mid_name'] + '\n')
        except Exception as e:
            print("Pipeline发生错误")
        return item

    def close_spider(self, follow_list):
        self.file.close()

class UpVideoPipeline(object):
    def __init__(self):
        try:
            self.file = open('follow_list.csv', 'r', encoding='utf8')
        except Exception:
            print('文件异常')

    def process_item(self, item, up_video):
        return item

    def close_spider(self, up_video):
        self.file.close()

class VideoInfoPipelie(object):
    # def __init__(self):
    #     self.file = open('follow_list.csv', 'r', encoding='utf8')
    #
    # def process_item(self, item, up_video):
    #
    #     return item
    #
    # def close_spider(self, up_video):
    #     self.file.close()
    pass


