# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Spider
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
from scrapy.http import Request

class TrySpider(Spider):
    name = 'try'
    allowed_domains = ['scholar.google.com']
    start_urls = ['https://scholar.google.co.id/citations?user=QLDyB0sAAAAJ&hl=id']

    def start_requests(self):
        self.driver = webdriver.Chrome('/home/arham/chromedriver_linux64/chromedriver')         
        self.driver.get('https://scholar.google.co.id/citations?user=QLDyB0sAAAAJ&hl=id')

        page = self.driver.find_element_by_xpath('//button[@class="gs_btnPD gs_in_ib gs_btn_flat gs_btn_lrge gs_btn_lsu"]')
        button = page.is_enabled()

        while button is True:
            page.click()
            print("Klik")
            if button is False:
                break
            print("Ulang")
            yield Request(callback=self.parse)

        # while True:
        #     try:
        #         next_page = self.driver.find_element_by_xpath('//button[@class="gs_btnPD gs_in_ib gs_btn_flat gs_btn_lrge gs_btn_lsu"]')
        #         sleep(5)
        #         self.logger.info('Sleeping for 5 sec')
        #         next_page.click()
 
                
        #     except NoSuchElementException:
        #         self.logger.info('No more pages')
        #         sel = Selector(text=self.driver.page_source)   
        #         self.logger.info('Finally gagal')
        #         break


    def parse(self, response):
        pass
