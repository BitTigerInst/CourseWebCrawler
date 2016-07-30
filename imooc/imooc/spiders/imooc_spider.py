__author__ = 'huafei'

import scrapy
import re
from scrapy.selector import Selector
from imooc.items import ImoocItem

class ImoocSpider(scrapy.Spider):
    name = "imooc"
    allowed_domains = ["imooc.com"]
    start_urls = ["http://www.imooc.com/course/list"]

    def parse(self, response):
        page = Selector(response)
        divs = page.xpath('//li[@class="course-one"]')
        base_urls = "http://www.imooc.com"
        for div in divs:
            item = ImoocItem()
            item['name'] = div.xpath('./a/h5/span/text()').extract_first().encode('utf-8')
            item['url'] = div.xpath('./a/@href').extract_first()
            num = div.xpath('./a/div[@class="tips"]/span[@class="l ml20"]/text()').extract_first().encode('utf-8')
            item['student_num'] = num.split()[0]
            item['intro'] = div.xpath('./a/div[@class="tips"]/p[@class="text-ellipsis"]/text()').extract_first().encode('utf-8')
            url = base_urls + item['url']
            print url
            req = scrapy.Request(url, callback=self.parse_detail_page)
            req.meta["item"] = item
            yield req

    def parse_detail_page(self, response):
        item = response.meta["item"]

        item['grade'] = response.xpath('//div[@class="satisfaction-degree-info"]/h4/text()').extract_first().encode('utf-8')
        item['discuss_num'] = response.xpath('//p[@class="person-num noLogin"]/a/text()').extract_first().encode('utf-8')
        yield item
