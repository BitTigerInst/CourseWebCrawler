
__author__ = 'huafei'

import scrapy
import re
import os
from scrapy.selector import Selector
from imooc.items import ImoocItem

class ImoocSpider(scrapy.Spider):
    name = "imooc"
    allowed_domains = ["imooc.com"]
    start_urls = ["http://www.imooc.com/course/list?page=2"]

    def __init__(self):
        file = open("./spiders/keyword.txt", 'r')
        self.keywords = []
        lines = file.readlines()
        for line in lines:
            self.keywords.append(line.strip())

    def extractKeywords(self, intro):
        keyword = ""
        first = True
        for k in self.keywords:
            if intro.lower().find(k.lower()) != -1:
                if first:
                    keyword = k
                else :
                    keyword = keyword + "|" + k
        return keyword

    def parse(self, response):
        page = Selector(response)
        divs = page.xpath('//div[@class="moco-course-wrap"]')
        base_urls = "http://www.imooc.com"
        for div in divs:
            item = ImoocItem()
            item['name'] = div.xpath('./a/div[@class="moco-course-box"]/div[@class="moco-course-intro"]/h3/text()').extract()[1].encode('utf-8').strip()
            print item['name']
            url = div.xpath('./a/@href').extract_first()
            item['url'] = base_urls + url
            print item['url']
            item['id'] = url.encode('utf-8').strip().split('/')[2]
            item['img_url'] = div.xpath('./a/div[@class="moco-course-box"]/img/@src').extract_first()
            print item['img_url']
            num = div.xpath('./a/div[@class="moco-course-box"]/div[@class="moco-course-bottom"]/span/text()').extract_first().encode('utf-8').strip()
            print num
            item['student_num'] = re.match(r'\d+', num).group(0).strip()
            item['intro'] = div.xpath('./a/div[@class="moco-course-box"]/div[@class="moco-course-intro"]/p/text()').extract_first().encode('utf-8').strip()
            print item['intro']
            item['platform'] = 'imooc'
            req = scrapy.Request(item['url'], callback=self.parse_detail_page)
            req.meta["item"] = item
            yield req

        curr_page = int(response.xpath('//div[@class="page"]/a[@class="active"]/text()').extract_first())
        if curr_page != 2:
            next_page_url = base_urls + "/course/list?page=" + str(curr_page + 1)
            print "next page is ", next_page_url
            request = scrapy.Request(next_page_url, callback=self.parse)
            yield request
        else:
            print "this is the end"

    def parse_detail_page(self, response):
        item = response.meta["item"]

        item['grade'] = response.xpath('//div[@class="score-info"]/div[@class="satisfaction-degree-info"]/h4/text()').extract_first().encode('utf-8').strip()
        print item['grade']
        discuss_num = response.xpath('//p[@class="person-num noLogin"]/a/text()').extract_first().encode('utf-8')
        item['discuss_num'] = re.match(r'\d+', discuss_num).group(0).strip()
        print item['discuss_num']
        item['intro_detail'] = response.xpath('//div[@class="content"]/div[@class="course-brief"]/p/text()').extract_first().encode('utf-8').strip()
        print item['intro_detail']
        item['keywords'] = self.extractKeywords(item['intro_detail'])
        print item['keywords']
        yield item
