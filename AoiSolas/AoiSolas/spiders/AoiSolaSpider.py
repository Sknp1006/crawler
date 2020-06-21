# -*- coding: utf-8 -*-

import scrapy
from urllib import parse
from AoiSolas.items import AoisolasItem


class AoisolaspiderSpider(scrapy.Spider):
    name = "AoiSola"
    allowed_domains = ["www.tupianzj.com"]
    start_urls = ['https://www.tupianzj.com/meinv/xiezhen/',
                  'https://www.tupianzj.com/meinv/xinggan/',
                  'https://www.tupianzj.com/meinv/guzhuang/',
                  'https://www.tupianzj.com/meinv/yishu/',
                  'https://www.tupianzj.com/meinv/siwa/',
                  'https://www.tupianzj.com/meinv/chemo/',
                  ]

    def parse(self, response):
        list = response.css(".list_con_box_ul li")
        for img in list:
            imgname = img.css("label::text").extract_first()
            imgurl = img.css("a::attr(href)").extract_first()
            imgurl2 = str(imgurl)
            imgurl2 = parse.urljoin(response.url, imgurl2)
            # print(imgurl2)
            cur_group = response.url.split('/')[-2]
            next_url = response.css("a:contains('下一页')::attr(href)").extract_first()
            next_url = parse.urljoin(response.url, next_url)

            if next_url is not None:
                # 下一页
                yield response.follow(next_url, callback=self.parse)

            yield scrapy.Request(imgurl2, callback=self.content, meta={"group": cur_group})

    def content(self, response):
        item = AoisolasItem()
        item['name'] = response.css(".bgff h1::text").extract_first()
        item['ImgUrl'] = response.css(".pic_tupian img::attr(src)").extract()
        item['group'] = response.meta['group']
        yield item
        # 提取图片,存入文件夹
        # print(item['ImgUrl'])
        next_url = response.css("a:contains('下一页')::attr(href)").extract_first()
        next_url = parse.urljoin(response.url, next_url)

        if next_url is not None:
            # 下一页
            yield scrapy.Request(next_url, callback=self.content, meta={"group": item['group']})

