# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import Request

from dznow.items import NewsItem


class TsaSpiderSpider(scrapy.Spider):
    name = 'TSA'
    allowed_domains = ['www.tsa-algerie.com']
    start_urls = [
        'https://www.tsa-algerie.com/economie/',
        'https://www.tsa-algerie.com/international/',
        "https://www.tsa-algerie.com/sport/",
        "https://www.tsa-algerie.com/videos/"
    ]

    def parse(self, response):
        for i in response.css(".category__highlighted-grid article"):
            item = NewsItem()
            item["resume"] = i.css(
                ".article-preview__desc ::text").get().strip()
            item["link"] = i.css("h1 a::attr(href)").get()
            item["title"] = i.css("h1 a::text").get()
            item["category"] = response.url.split("/")[-2:-1][0]
            item["image"] = i.css("a ::attr(data-bg)").get()
            yield Request(item['link'], self.parse_item, meta={"item": item})

    def parse_item(self, response):
        item = response.meta['item']
        content = response.css(".article__highlighted p::text").getall()
        item["content"] = " ".join(x for x in content)
        item["date"] = response.css("time::attr(datetime)").get()
        item["date"] = datetime.datetime.strptime(item["date"][:-6],
                                                  "%Y-%m-%dT%X")

        item["video"] = response.css("iframe::attr(src)").get()
        if 'Cet article est ' in item["content"]:
            return
        yield item
