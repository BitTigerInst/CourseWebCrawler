# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class ImoocPipeline(object):
    def __init__(self):
        self.file = open('imooc.dat', 'wb')

    def process_item(self, item, spider):
        val = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n".format(item['cid'], item['name'], item['score'], item['platform'], item['url'], item['keywords'], item['review_num'], item['student_num'], item['intro'], item['img_url'], item['intro_detail'])
        self.file.write(val)
        return item

class ImoocMongodbPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = "courses"
        self.db[collection_name].insert(dict(item))
        return item
