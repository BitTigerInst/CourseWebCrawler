# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ImoocPipeline(object):
    def __init__(self):
        self.file = open('imooc.dat', 'wb')

    def process_item(self, item, spider):
        val = "{0}\t{1}\t{2}\t{3}\n".format(item['name'], item['intro'], item['student_num'], item['url'])
        self.file.write(val)
        return item
