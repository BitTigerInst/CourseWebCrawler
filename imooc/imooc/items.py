# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ImoocItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    intro = scrapy.Field()
    student_num = scrapy.Field()
    discuss_num = scrapy.Field()
    grade = scrapy.Field()
    img_url = scrapy.Field()
    intro_detail = scrapy.Field()
    platform = scrapy.Field()
    keywords = scrapy.Field()
    pass
