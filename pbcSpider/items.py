# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PbcspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    dateStr = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    isImportant = scrapy.Field()

    pass
