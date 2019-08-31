# -*- coding: utf-8 -*-
import scrapy


class ApsSpider(scrapy.Spider):
    name = 'aps'
    allowed_domains = ['http://www.aps.dz/rss']
    start_urls = ['http://http://www.aps.dz/rss/']

    def parse(self, response):
        pass
