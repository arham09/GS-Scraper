# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Spider
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
from scrapy.http import Request


class AllSpider(Spider):
    name = 'all'
    allowed_domains = ['scholar.google.com']
    start_urls = ['https://scholar.google.com/citations?view_op=view_org&hl=id&org=1388872056037598937']

    def parse(self, response):
        self.driver = webdriver.Chrome('/home/arham/Webdriver/chromedriver_linux64/chromedriver')         
        self.driver.get(response.url)

        sel = Selector(text=self.driver.page_source)    
        users = sel.xpath('//div[@id="gsc_sa_ccl"]/div[@class="gsc_1usr gs_scl"]/div[@class="gsc_oai"]/h3[@class="gsc_oai_name"]/a/@href').extract()
        
        for user in users:
            url = 'https://scholar.google.com' + user
            yield {
                "user": user,
                "url": url
            }

        while True:
            next_page = self.driver.find_element_by_xpath('//button[@class="gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx"]')
            if next_page.is_enabled() is True:    
                sleep(2)
                self.logger.info('Sleeping for 5 sec')
                next_page.click()

                sel = Selector(text=self.driver.page_source)    
                users = sel.xpath('//div[@id="gsc_sa_ccl"]/div[@class="gsc_1usr gs_scl"]/div[@class="gsc_oai"]/h3[@class="gsc_oai_name"]/a/@href').extract()
        
                for user in users:
                    url = 'https://scholar.google.com' + user
                    yield {
                        "user": user,
                        "url": url
                    }
                    sleep(2)
            else:
                self.logger.info("No More Pages")
                break
