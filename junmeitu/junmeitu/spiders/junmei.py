import scrapy
import re
from urllib import parse
from junmeitu.items import JunmeituItem


class JunmeiSpider(scrapy.Spider):
    name = 'junmei'
    allowed_domains = ['junmeitu.com']
    start_urls = ['https://junmeitu.com/model/index.html']

    def parse(self, response):
        people_list = response.css(".people-list li")
        base_url = "/".join(response.url.split('/')[:-1]) + "/"
        # print(people_list)
        for img in people_list:
            modelname = img.css('img::attr(alt)').extract_first()  # 模特名字
            # imgurl = img.css('img::attr(src)').extract_first()  # 图片封面地址
            img_page = img.css('a::attr(href)').extract_first()  # 模特详情页
            cur_group = response.url.split('/')[-2]  # 当前分类

            model_page = parse.urljoin(base_url, img_page)
            yield scrapy.Request(model_page, callback=self.content, meta={"group": cur_group, "name": modelname})

        # 下一页
        cur_index = 1 if len(response.url.split('/')[-1].split('-')) == 1 else int(
            re.search("\d+", response.url.split('/')[-1]).group())
        next_page = "index-{}.html".format(cur_index + 1)
        next_url = parse.urljoin(base_url, next_page)
        if cur_index + 1 <= 100:
            yield response.follow(next_url, callback=self.parse)

    def content(self, response):
        """个人页"""
        albums = response.css(".pic-list li")
        for album in albums:
            album_url = album.css('a::attr(href)').extract_first()
            album_name = album.css('img::attr(alt)').extract_first()
            album_page = parse.urljoin("https://junmeitu.com", album_url)
            yield scrapy.Request(album_page, callback=self.info,
                                  meta={"album": album_name,
                                        "group": response.meta['group'],
                                        "modelname": response.meta['name']})

        next_url = response.css("a:contains('下一页')::attr(href)").extract_first()
        next_url = parse.urljoin(response.url, next_url)
        if response.url == next_url:
            return
        elif len(next_url) == 0:
            return
        else:
            yield response.follow(next_url, callback=self.content, meta={"group": response.meta['group'],
                                                                         "name": response.meta['name']})

    def info(self, response):
        """图片详情页"""
        i = JunmeituItem()
        i['name'] = response.meta['album']
        i['ImgUrl'] = response.css(".pictures img::attr(src)").extract_first()
        i['group'] = response.meta['group']
        i['modelName'] = response.meta['modelname']
        yield i

        next_url = response.css("a:contains('下一页')::attr(href)").extract_first()
        next_url = parse.urljoin(response.url, next_url)
        if response.url == next_url:
            return
        elif len(next_url) == 0:
            return
        else:
            yield scrapy.Request(next_url, callback=self.info, meta={"group": response.meta['group'],
                                                                      "modelname": response.meta['modelname'],
                                                                      "album": response.meta['album']})
