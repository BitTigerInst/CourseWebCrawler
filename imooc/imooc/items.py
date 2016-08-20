# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ImoocItem(scrapy.Item):
    # define the fields for your item here like:
    cid = scrapy.Field()
    name = scrapy.Field()
    score = scrapy.Field()
    platform = scrapy.Field()
    url = scrapy.Field()
    keywords = scrapy.Field()
    student_num = scrapy.Field()
    review_num = scrapy.Field()
    intro = scrapy.Field()
    img_url = scrapy.Field()
    intro_detail = scrapy.Field()

    pass
