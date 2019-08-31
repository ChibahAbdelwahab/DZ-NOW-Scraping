# -*- coding: utf-8 -*-
import datetime

import scrapy
import re

from scrapy import Request
from scrapy.http import TextResponse

from dznow.items import NewsItem


class ApsSpider(scrapy.spiders.XMLFeedSpider):
    name = 'aps'
    start_urls = ['http://feeds.aps.dz/aps-algerie',
                  "http://feeds.aps.dz/aps-economie",
                  "http://feeds.aps.dz/aps-monde",
                  "http://feeds.aps.dz/aps-sport",
                  "http://feeds.aps.dz/aps-societe",
                  "http://feeds.aps.dz/aps-culture",
                  "http://feeds.aps.dz/aps-societe",
                  "http://feeds.aps.dz/aps-culture",
                  "http://feeds.aps.dz/aps-regions",
                  "http://feeds.aps.dz/APS-Sante-Science-Technologie",
                  ]
    itertag = 'item'
    custom_settings = {
        "HTTPCACHE_ENABLED": 'True'
    }
    headers = {
        # "Host": "http://www.aps.dz",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36:",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3:",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate:",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6:",
        "Connection": "keep-alive:",
    }

    def parse_node(self, response, node):
        item = NewsItem()
        item['title'] = node.xpath('title/text()').get()
        item['link'] = node.xpath('link/text()').get()
        description = node.xpath('description/text()').get()
        description = TextResponse(response.url, body=description,
                                   encoding='utf-8')
        item['category'] = node.xpath('category/text()').get()
        item['author'] = node.xpath('author/text()').get()
        item['date'] = datetime.datetime.strptime(
            node.xpath("pubDate/text()").get(), '%a, %d %b %Y %X +%f')
        yield Request(item['link'], self.parse_item, headers=self.headers,
                      meta={"item": item})

    def parse_item(self, response):
        item = response.meta["item"]
        item["title"] = response.css(".itemTitle ::text").get()
        item["resume"] = response.css(".itemIntroText::text").get()
        item["image"] = response.css(".itemImage img ::attr(src)").get()
        item["content"] = response.css(".itemFullText::text").get()
        yield item
