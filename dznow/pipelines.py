# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DznowPipeline(object):
    def process_item(self, item, spider):
        item["source"] = spider.name
        item["content"].strip()
        item["resume"].replace("\r", '').replace("\n", "").strip()
        return item
