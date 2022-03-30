# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JunmeituItem(scrapy.Item):
    name = scrapy.Field()
    ImgUrl = scrapy.Field()
    group = scrapy.Field()
    modelName = scrapy.Field()
    image_paths = scrapy.Field()
