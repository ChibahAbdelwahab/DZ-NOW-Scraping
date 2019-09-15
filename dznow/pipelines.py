# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DznowPipeline(object):
    def process_item(self, item, spider):
        item["source"] = spider.name
        try:
            content = "".join(str(x).strip() for x in item["content"])
            item['content'] = content
        except:
            pass
        try:
            item["content"] = item["content"].strip()
        except:
            pass
        return item
