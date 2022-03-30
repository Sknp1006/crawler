# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import re


class JunmeituPipeline(ImagesPipeline):

    #
    # def file_path(self, request, response=None, info=None):
    #     """
    #     :param request: 每一个图片下载管道请求
    #     :param response:
    #     :param info:
    #     :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
    #     :return: 每套图的分类目录
    #     """
    #     item = request.meta['item']
    #     folder = item['name']
    #
    #     folder_strip = re.sub(r'[？\\*|“<>:/]', '', str(folder))
    #     image_guid = request.url.split('/')[-1]
    #     filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
    #     return filename

    # 1
    def get_media_requests(self, item, info):
        yield Request(item['ImgUrl'], meta={'item': item['name'], 'group': item['group'], 'modelname': item['modelName']})

    # 2
    def file_path(self, request, response=None, info=None):
        name = request.meta['item']
        modelname = request.meta['modelname'].strip()
        # name = filter(lambda x: x not in '()0123456789', name)
        # name = re.sub(r'[？\\*|“<>:/()0123456789]', '', name)  # 去除括号
        image_guid = request.url.split('/')[-1]
        group = request.meta['group']
        # name2 = request.url.split('/')[-2]
        filename = u'{0}/{1}/{2}/{3}'.format(group, modelname, name, image_guid)
        return filename

    # 3
    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path
        return item
