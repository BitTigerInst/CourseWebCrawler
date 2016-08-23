__author__ = 'Xiao Liu'
# -*- coding: utf-8 -*-  
# How to fix: "UnicodeDecodeError: 'ascii' codec can't decode byte"
# http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import scrapy
import re, os, string, json, time
from w3lib.url import add_or_replace_parameter
from scrapy.selector import Selector
from mooc_crawler.items import MoocCrawlerItem

class ClassCentralSpider(scrapy.Spider):
    name = "classCentral"
    allowed_domains = ["class-central.com"]
    start_urls = ["https://www.class-central.com/courses/past"]
    #start_urls = ["https://www.class-central.com/courses/recentlyAdded"]
    handle_httpstatus_list = [301]

    def __init__(self):
        file = open("./spiders/keyword.txt", 'r')
        lines = file.readlines()
        self.keywords = [line.lower().strip() for line in lines]
        #print "keywords: ", self.keywords
        self.total_item_num = 0
        self.steps = -1
        self.flag = True
        self.cnt = 1


    def get_keywords(self, intro):
        intro = set(re.split(r'[.;,\s]', intro.lower())) - {''}
        return [kw for kw in self.keywords if kw in intro]


    def parse(self, response):
        # Get help from:  http://stackoverflow.com/questions/38574869/how-can-i-jump-to-next-page-in-scrapy
        if response.meta.get('is_json', False):
            page = Selector(text=json.loads(response.body)['table'])
        else:
            page = Selector(response) 

        if self.flag:
            self.total_item_num = int(page.xpath('//div[@id="show-more-courses"]/text()').re(r'courses of (.*)')[0]) + 50
            print "Total courses: ", self.total_item_num
            self.steps = self.total_item_num / 50 + 1
            self.flag = False

        base_urls = "https://www.class-central.com/courses/past"
        #base_urls = "https://www.class-central.com/courses/recentlyAdded"
        my_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

        divs = page.xpath('//tr[@itemtype="http://schema.org/Event"]')
        #print "print content", len(divs) 
        print "Process: ", self.cnt, '/', self.steps

        for div in divs:
            item = MoocCrawlerItem()
            item = {k:"" for k in item.keys()}

            parse_name = div.xpath('./td/a/span[@class="course-name-text"]/text()').extract_first().strip()
            item['name'] = parse_name
            parse_score = div.xpath('./td/div[@class="course-rating-value"]/text()').extract_first().strip()
            if len(parse_score) > 3:
                parse_score = parse_score[:3]
            item['score'] = string.atof(parse_score) * 2
            parse_platform = div.xpath('./td/div[@class="course-provider"]/text()').extract_first().strip()
            item['platform'] = parse_platform
            parse_url = div.xpath('./td/a/@href').extract_first().decode().encode('utf-8').strip()
            item['url'] = "https://www.class-central.com" + parse_url
            parse_cid = re.findall(r'/mooc/(.*)/', parse_url)[0]
            item['cid'] = "cc" + parse_cid

            req = scrapy.Request(item['url'], headers=my_header, callback=self.parse_detail_page)
            req.meta['item'] = item   

            yield req
        
        #next_page_el = respones.xpath("//div[@id='show-more-courses']")

        if self.cnt < self.steps:
        #if next_page_el:
            next_page_url = "https://www.class-central.com/maestro/courses/past?page=1&_=1471346096733"
            #next_page_url = "https://www.class-central.com/maestro/courses/recentlyAdded?page=1"
            next_page = response.meta.get('page', 1) + 1
            next_page_url = add_or_replace_parameter(next_page_url, 'page', next_page)
            r = scrapy.Request(next_page_url, headers=my_header, callback=self.parse, meta={'page': next_page, 'is_json': True})
            self.cnt += 1
            yield r


    def parse_detail_page(self, response):
        """
        Get details for each course
        """
        item = response.meta['item']

        parse_review_num = response.xpath('//span[@itemprop="votes"]/text()').extract_first().strip()
        item['review_num'] = string.atoi(parse_review_num)

        parse_student_num = re.findall(r'"mycourses-listed-count", 0, (.*), 0', response.text)[0].strip() or '0'
        item['student_num'] = string.atoi(parse_student_num)

        parse_course_info = response.xpath('//div[@class="course-desc"]').extract()
        for i in range(len(parse_course_info) - 1):
            parse_course_info[0].extend(parse_course_info[i+1])
        item['keywords'] = self.get_keywords(parse_course_info[0]+item['name']) or []

        yield item

