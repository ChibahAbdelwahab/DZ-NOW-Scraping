# -*- coding: utf-8 -*-
import scrapy


class UpdateSpider(scrapy.Spider):
    name = 'update'
    allowed_domains = ['https://dznow1.herokuapp.com/dznowapi/update']
    start_urls = ['https://dznow1.herokuapp.com/dznowapi/update']

    def parse(self, response):
        pass
