# -*- coding: utf-8 -*-

import scrapy


class AoisolasItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    ImgUrl = scrapy.Field()
    group = scrapy.Field()
    image_paths = scrapy.Field()

    pass
