
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
            item['name'] = div.xpath('./a/h5/span/text()').extract_first().encode('utf-8').strip()
            item['url'] = div.xpath('./a/@href').extract_first()
            item['img_url'] = div.xpath('./a/div[@class="course-list-img"]/img/@src').extract_first()
            num = div.xpath('./a/div[@class="tips"]/span[@class="l ml20"]/text()').extract_first().encode('utf-8')
            item['student_num'] = num.split()[0]
            item['intro'] = div.xpath('./a/div[@class="tips"]/p[@class="text-ellipsis"]/text()').extract_first().encode('utf-8').strip()
            url = base_urls + item['url']
            print url
            req = scrapy.Request(url, callback=self.parse_detail_page)
            req.meta["item"] = item
            yield req

        curr_page = int(response.xpath('//div[@class="page"]/a[@class="active"]/text()').extract_first())
        if curr_page != 29:
            next_page_url = base_urls + "/course/list?page=" + str(curr_page + 1)
            print "next page is ", next_page_url
            request = scrapy.Request(next_page_url, callback=self.parse)
            yield request
        else:
            print "this is the end" 

    def parse_detail_page(self, response):
        item = response.meta["item"]

        item['grade'] = response.xpath('//div[@class="satisfaction-degree-info"]/h4/text()').extract_first().encode('utf-8').strip()
        discuss_num = response.xpath('//p[@class="person-num noLogin"]/a/text()').extract_first().encode('utf-8')
        item['discuss_num'] = re.match(r'\d+', discuss_num).group(0).strip()
        yield item
