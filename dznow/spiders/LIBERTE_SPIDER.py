# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import Request

from dznow.items import NewsItem


class LiberteSpiderSpider(scrapy.spiders.XMLFeedSpider):
    name = 'LIBERTE_SPIDER'
    start_urls = ['https://www.liberte-algerie.com/article/feed/']
    itertag = 'item'
    custom_settings = {
        "HTTPCACHE_ENABLED": 'True'
    }

    def parse_node(self, response, node):
        item = NewsItem()
        item['title'] = node.xpath('title/text()').get()
        item['link'] = node.xpath('link/text()').get()
        # item['content'] = node.xpath('description/text()').get()
        item['resume'] = node.xpath('description/text()').get()
        item["date"] = datetime.datetime.strptime(
            node.xpath("pubDate/text()").get(), '%a, %d %b %Y %X +%f')
        yield Request(item["link"], self.parse_item, meta={"item": item})

    def parse_item(self, response):
        item = response.meta["item"]
        item["content"] = "".join(
            str(x) for x in response.css("#text_core p::text").getall()
        )
        item["category"] = response.css("#global strong::text").get().strip()
        item["image"] = response.css(".post-image ::attr(src)").get()
        yield item
