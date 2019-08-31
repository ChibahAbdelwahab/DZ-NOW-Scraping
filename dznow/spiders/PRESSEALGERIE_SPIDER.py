# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import TextResponse

from dznow.items import NewsItem


class PressealgerieSpiderSpider(scrapy.spiders.XMLFeedSpider):
    name = 'PRESSEALGERIE_SPIDER'
    allowed_domains = ['http://www.pressealgerie.fr/news/feed/']
    start_urls = ['http://www.pressealgerie.fr/news/feed//']
    itertag = 'item'
    custom_settings = {
        "HTTPCACHE_ENABLED": 'True'
    }

    def parse_node(self, response, node):
        item = NewsItem()
        item["title"] = node.xpath("title/text()").get()
        item["link"] = node.xpath("link/text()").get()
        item["date"] = node.xpath("pubDate/text()").get()
        item["category"] = node.xpath("category/text()").get()
        item["author"] = node.xpath("dc/author/text()").get()
        item["category"] = node.xpath("category/text()").get()
        description = node.xpath("description/text()").get()
        description = TextResponse(response.url, body=description,
                                   encoding='utf-8')
        item["image"] = description.css("img ::attr('src')").get()
        item["content"] = get_description(
            description.css(":not(script)::text").getall())
        item["resume"] = item["content"]
        yield item


def get_description(data):
    for i in data:
        if len(i.strip()) > 0:
            return i.strip()
