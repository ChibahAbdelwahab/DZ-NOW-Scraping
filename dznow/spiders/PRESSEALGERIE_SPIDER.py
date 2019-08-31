# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http import TextResponse

from dznow.items import NewsItem
import datetime


class PressealgerieSpiderSpider(scrapy.spiders.XMLFeedSpider):
    name = 'PRESSEALGERIE_SPIDER'
    start_urls = ['http://www.pressealgerie.fr/news/feed/']
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
        item["title"] = node.xpath("title/text()").get()
        item["link"] = node.xpath("link/text()").get()
        item["date"] = datetime.datetime.strptime(
            node.xpath("pubDate/text()").get(), '%a, %d %b %Y %X +%f')
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
        yield Request(item["link"], self.parse_item, meta={"item": item})

    def parse_item(self, response):
        item = response.meta["item"]
        item["content"] = "".join(
            str(x) for x in response.css("article p::text").getall())
        images = []
        for i in enumerate(
                response.css(".rgg-imagegrid a::attr(href)").getall()):
            images.append(i)
        item["extra_images"] = images
        yield item


def get_description(data):
    for i in data:
        if len(i.strip()) > 0:
            return i.strip()
