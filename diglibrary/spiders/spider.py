#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import Request
from w3lib.html import remove_tags

from diglibrary.utils.log import *
from diglibrary.items import BookItem

class LibrarySpider(CrawlSpider):
    name = 'diglibrary'
    max_num = 170000
    allowed_domains = ['210.30.108.79']
    #start_urls = ['http://210.30.108.79/opac/']
    rules = [
        Rule(LinkExtractor(allow=['/opac/item.php?marc_no=\d+']), callback='parse_book_first'),
        Rule(LinkExtractor(allow=['/opac/show_format_marc.php?marc_no=\w+']), callback='parse_book_second')
    ]

    def __init__(self, *args, **kwargs):
        self.start_urls = self.generate_url(self.max_num)
        #self.start_urls = ['http://210.30.108.79/opac/item.php?marc_no=0000001000']
        super(LibrarySpider, self).__init__(*args, **kwargs)

    def generate_url(self,max_num):
        base_url='http://210.30.108.79/opac/item.php?marc_no='
        for i in xrange(1,max_num):
            tmp = str(i)
            len_tmp = len(tmp)
            if len_tmp < 10:
                num_part = (10 - len_tmp)*'0' + tmp
                yield base_url + num_part

    def parse(self, response):
        item = BookItem()
        item['marc_no'] = int(response.url.split('=')[-1])
        info("crawling " + str(item['marc_no']))
        item['location'] = response.xpath(r"//*[@id='item']/tr[2]/td[4]").extract()
        if len(item['location']) == 0:
            return []
        else:
            item['location'] = remove_tags(item['location'][0].strip())[11:-5]
        detail_url = response.xpath(r"//*[@id='tabs1']/ul/li[2]/a/@href").extract()[0].strip()
        language_type = response.xpath('//*[@id="marc"]/text()').extract()[-1]
        request = Request('http://210.30.108.79/opac/'+detail_url, callback=self.parse_book_second)
        if "中文".decode('utf-8') in language_type:
            request.meta['language_type'] = 'zh'
        elif "西文".decode('utf-8') in language_type:
            request.meta['language_type'] = 'en'
        else:
            warn(item['marc_no'])
            return []
        request.meta['item'] = item
        return request

    def parse_book_first(self, response):
        item = BookItem()
        item['marc_no'] = int(response.url.split('=')[-1])
        info("crawling " + str(item['marc_no']))
        item['location'] = response.xpath(r"//*[@id='item']/tr[2]/td[4]/text()").extract()
        if len(item['location']) == 0:
            return []
        else:
            item['location'] = item['location'][0].strip()
        detail_url = response.xpath(r"//*[@id='tabs1']/ul/li[2]/a/@href").extract()[0].strip()
        language_type = response.xpath('//*[@id="marc"]/text()').extract()[-1]
        request = Request('http://210.30.108.79/opac/'+detail_url, callback=self.parse_book_second)
        if "中文".decode('utf-8') in language_type:
            request.meta['language_type'] = 'zh'
        elif "西文".decode('utf-8') in language_type:
            request.meta['language_type'] = 'en'
        else:
            warn(item['marc_no'])
            return []
        request.meta['item'] = item
        return request

    def parse_book_second(self, response):
        item = response.meta['item']
        language_type = response.meta['language_type']
        if language_type == 'en':
            row020 = response.xpath('/html/body/div/ul/li[contains(b,"020")]').extract()
            if len(row020) > 0:
                row020 = remove_tags(row020[0]).split('|')
                for i in row020:
                    if i[0] == 'a':
                        if len(i) < 3:
                            item['isbn'] = ''
                        else:
                            if i[2] == ' ':
                                item['isbn'] = ''
                            else:
                                item['isbn'] = i[2:].split()[0].replace('-','')
            else:
                item['isbn'] = ''
            row245 = response.xpath('/html/body/div/ul/li[contains(b,"245")]').extract()[0].strip()
            row260 = response.xpath('/html/body/div/ul/li[contains(b,"260")]').extract()[0].strip()
            row093 = response.xpath('/html/body/div/ul/li[contains(b,"093")]').extract()[0].strip()
            row245 = row245.split('|')
            row260 = row260.split('|')
            row093 = row093.split('|')
            for i in row245:
                if i[0] == 'a':
                    item['booktitle'] = remove_tags(i[2:])
                if i[0] == 'c':
                    item['author'] = remove_tags(i[2:])
            for i in row260:
                if i[0] == 'b':
                    item['press'] = remove_tags(i[2:])
                if i[0] == 'c':
                    item['publication_date'] = remove_tags(i[2:])
            for i in row093:
                if i[0] == 'a':
                    item['call_number'] = remove_tags(i[2:])
            return item
        elif language_type == 'zh':
            row010 = response.xpath('/html/body/div/ul/li[contains(b,"010")]').extract()
            if len(row010) > 0:
                row010 = remove_tags(row010[0]).split('|')
                for i in row010:
                    if i[0] == 'a':
                        if len(i) < 3:
                            item['isbn'] = ''
                        else:
                            if i[2] == ' ':
                                item['isbn'] = ''
                            else:
                                item['isbn'] = i[2:].split()[0].replace('-','')
            else:
                item['isbn'] = ''
            row200 = response.xpath('/html/body/div/ul/li[contains(b,"200")]').extract()[0].strip()
            row210 = response.xpath('/html/body/div/ul/li[contains(b,"210")]').extract()[0].strip()
            row905 = response.xpath('/html/body/div/ul/li[contains(b,"905")]').extract()[0].strip()
            row200 = row200.split('|')
            row210 = row210.split('|')
            row905 = row905.split('|')
            for i in row200:
                if i[0] == 'a':
                    item['booktitle'] = remove_tags(i[2:])
                if i[0] == 'f':
                    item['author'] = remove_tags(i[2:])
            for i in row210:
                if i[0] == 'c':
                    item['press'] = remove_tags(i[2:])
                if i[0] == 'd':
                    item['publication_date'] = remove_tags(i[2:])
            for i in row905:
                if i[0] == 'd':
                    item['call_number'] = remove_tags(i[2:])
            return item
