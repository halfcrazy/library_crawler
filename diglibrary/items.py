#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BookItem(scrapy.Item):
    # define the fields for your item here like:
    booktitle = scrapy.Field()
    author = scrapy.Field()
    press = scrapy.Field()
    publication_date = scrapy.Field()
    call_number = scrapy.Field()
    marc_no = scrapy.Field()
    location = scrapy.Field()
