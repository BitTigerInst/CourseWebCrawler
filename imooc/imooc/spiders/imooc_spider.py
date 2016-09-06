
__author__ = 'huafei'

import scrapy
import re
import string
import os
from scrapy.selector import Selector
from imooc.items import ImoocItem

class ImoocSpider(scrapy.Spider):
    name = "imooc"
    allowed_domains = ["imooc.com"]
    start_urls = ["http://www.imooc.com/course/list"]

    def __init__(self):
        file = open("./spiders/keyword.txt", 'r')
        self.keywords = []
        lines = file.readlines()
        for line in lines:
            self.keywords.append(line.strip())
        print self.keywords

    def extractKeywords(self, intro):
        keyword = []
        for k in self.keywords:
            if intro.lower().find(k.lower()) != -1:
                keyword.append(k)
        return keyword

    def parse(self, response):
        page = Selector(response)
        divs = page.xpath('//div[@class="moco-course-wrap"]')
        base_urls = "http://www.imooc.com"
        for div in divs:
            item = ImoocItem()
            name = div.xpath('./a/div[@class="moco-course-box"]/div[@class="moco-course-intro"]/h3/text()').extract()
            if len(name) == 0:
                continue
            item['name'] = name[1].encode('utf-8').strip()
            url = div.xpath('./a/@href').extract_first()
            item['url'] = base_urls + url
            cid = url.encode('utf-8').strip().split('/')[2]
            item['cid'] = "im" + cid
            item['img_url'] = div.xpath('./a/div[@class="moco-course-box"]/img/@src').extract_first()
            num = div.xpath('./a/div[@class="moco-course-box"]/div[@class="moco-course-bottom"]/span/text()').extract_first().encode('utf-8').strip()
            student_num = re.match(r'\d+', num).group(0).strip()
            item['student_num'] = string.atoi(student_num)
            item['intro'] = div.xpath('./a/div[@class="moco-course-box"]/div[@class="moco-course-intro"]/p/text()').extract_first().encode('utf-8').strip()
            item['platform'] = 'imooc'
            req = scrapy.Request(item['url'], callback=self.parse_detail_page)
            req.meta["item"] = item
            yield req

        curr_page = int(response.xpath('//div[@class="page"]/a[@class="active"]/text()').extract_first())
        if curr_page != 24:
            next_page_url = base_urls + "/course/list?page=" + str(curr_page + 1)
            print "next page is ", next_page_url
            request = scrapy.Request(next_page_url, callback=self.parse)
            yield request
        else:
            print "this is the end"

    def parse_detail_page(self, response):
        item = response.meta["item"]

        score = response.xpath('//div[@class="statics clearfix"]/div[@class="static-item l score-btn"]/span[@class="meta-value"]/text()').extract_first().encode('utf-8').strip()
        item['score'] = string.atof(score)
        review_num = response.xpath('//div[@class="score-box"]/a[@class="person-num"]/span/text()').extract_first().encode('utf-8').strip()
        review_num = re.match(r'\d+', review_num).group(0).strip()
        item['review_num'] = string.atoi(review_num)
        item['intro_detail'] = response.xpath('//div[@class="content"]/div[@class="course-brief"]/p/text()').extract_first().encode('utf-8').strip()
        intro = item['name'] + item['intro'] + item['intro_detail']
        item['keywords'] = self.extractKeywords(intro)
        print item['keywords']
        yield item
