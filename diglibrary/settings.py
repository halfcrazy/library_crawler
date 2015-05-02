#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# Scrapy settings for diglibrary project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#


BOT_NAME = 'diglibrary'

SPIDER_MODULES = ['diglibrary.spiders']
NEWSPIDER_MODULE = 'diglibrary.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5"

ITEM_PIPELINES = {
    'diglibrary.pipelines.DuplicatesPipeline':100,
    #'diglibrary.pipelines.Save2DBPipeline':200,
    'diglibrary.pipelines.JsonWithEncodingPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
    'diglibrary.middleware.ErrorMonkeyMiddleware': 1,
}

# LOG_LEVEL = 'INFO'
# LOG_LEVEL = 'DEBUG'
LOG_LEVEL = 'ERROR'
