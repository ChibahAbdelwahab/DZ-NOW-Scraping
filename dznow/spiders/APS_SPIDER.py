# -*- coding: utf-8 -*-
import scrapy
import re

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
                  "http://feeds.aps.dz/APS-Sante-Science-Technologie", ]
    itertag = 'item'
    custom_settings = {
        "HTTPCACHE_ENABLED": 'True'
    }

    def parse_node(self, response, node):
        item = NewsItem()
        item['title'] = node.xpath('title/text()').get()
        item['link'] = node.xpath('link/text()').get()
        description = node.xpath('description/text()').get()
        description = TextResponse(response.url, body=description,
                                   encoding='utf-8')
        item['image'] = description.css("div img ::attr('src')").get()
        item['resume'] = description.css(".K2FeedIntroText strong::text").get()
        item['content'] = description.css(".K2FeedFullText ::text ").getall()
        item['category'] = node.xpath('category/text()').get()
        item['author'] = node.xpath('author/text()').get()
        return item
