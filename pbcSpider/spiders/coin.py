import scrapy
import re
import os
import pickle
from collections import deque
from pbcSpider.items import PbcspiderItem
from pbcSpider import settings
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.pbc.gov.cn']
    start_urls = ['http://www.pbc.gov.cn/huobijinyinju/147948/147964/22786/index1.html']

    regexp = re.compile(settings.PBCCOIN_IMPORTANT, re.IGNORECASE)
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    splash_args = {
        'wait': 5
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                args=self.splash_args,
                                callback=self.parse)

    def parse(self, response):
        cacheLocal = settings.PBCCOIN_CACHE_LOCAL

        try:
            if os.path.getsize(cacheLocal) > 0:
                eventsQueue = pickle.load(open(cacheLocal, 'rb'))
                self.logger.info("eventsQueue read successfully!")
            else:
                eventsQueue = deque(maxlen=200)
                self.logger.info("eventsQueue is empty!")
        except:
            eventsQueue = deque(maxlen=200)
            self.logger.info("eventsQueue is error!")

        self.logger.info(
            "eventsQueue size before this run: {}".format(len(eventsQueue)))
        self.logger.info("eventsQueue :")
        self.logger.info(eventsQueue)

        targetDateTb = response.css("html body div.mainw950 table tbody tr td table tbody tr td div#r_con.column div.portlet div div table tbody tr td table tbody tr td span::text").extract()
        targetHrefTb = response.css("html body div.mainw950 table tbody tr td table tbody tr td div#r_con.column div.portlet div div table tbody tr td table tbody tr td font.newslist_style a::attr(href)").getall()
        targetTitleTb = response.css("html body div.mainw950 table tbody tr td table tbody tr td div#r_con.column div.portlet div div table tbody tr td table tbody tr td font.newslist_style a::attr(title)").getall()

        for tempDate, tempHref, tempTitle in zip(targetDateTb, targetHrefTb, targetTitleTb):
            self.logger.info(tempTitle)
            cacheItem = "{0}\n{1}\n".format(tempDate, tempTitle)
            if cacheItem not in eventsQueue:
                yield SplashRequest(url="http://www.pbc.gov.cn"+tempHref,
                                    meta={"dateStr": tempDate,
                                          "url": "http://www.pbc.gov.cn"+tempHref,
                                          "title": tempTitle},
                                    args=self.splash_args,
                                    callback=self.sub_parse)

                eventsQueue.append(cacheItem)

        self.logger.info(
            "eventsQueue size after this run: {}".format(len(eventsQueue)))
        self.logger.info("eventsQueue :")
        self.logger.info(eventsQueue)
        pickle.dump(eventsQueue, open(cacheLocal, 'wb'),
                    pickle.HIGHEST_PROTOCOL)

    def sub_parse(self, response):

        targetContents = response.css("html body div.mainw950 div.pre.column div.portlet div div table tbody tr td table tbody tr td table tbody tr td.content div p").getall()
        targetContent = "\n".join(targetContents)
        targetContent = re.sub(self.CLEANR, '', targetContent)

        newsItem = PbcspiderItem()
        newsItem['dateStr'] = response.meta["dateStr"]
        newsItem['url'] = response.meta["url"]
        newsItem['title'] = response.meta["title"]
        newsItem['content'] = targetContent

        if self.regexp.search(newsItem['title']):
            newsItem['isImportant'] = "True"
            self.logger.info("Important news:" + newsItem['title'])
        else:
            newsItem['isImportant'] = "False"

        yield newsItem

