# -*- coding: utf-8 -*-


from scrapy import signals


class AoisolasSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        '''设置headers和切换请求头'''
        referer = request.url
        if referer:
            request.headers['referer'] = referer