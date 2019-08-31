# -*- coding: utf-8 -*-
import scrapy

from dznow.items import NewsItem
import datetime


class Algerie360SpiderSpider(scrapy.Spider):
    name = 'ALGERIE360'
    allowed_domains = ['https://www.algerie360.com/rss-feedburner/']
    start_urls = ['https://www.algerie360.com/rss-feedburner//']

    def parse(self, response):
        for i in response.css(".contentdiv"):
            item = NewsItem()
            item["title"] = i.css("a::attr('title')").get()
            item["link"] = i.css("a::attr('href')").get()
            # item["content"] = i.css("a::text").get()
            # item["resume"] = i.css("a::text").get()
            item["date"] = datetime.date.today()
            item["category"] = 'Actualité'
            yield item
