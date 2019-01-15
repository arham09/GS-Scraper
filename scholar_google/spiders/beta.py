# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Spider
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
from scrapy.http import Request

class ScholarSpider(Spider):
    name = 'scholar'
    allowed_domains = ['scholar.google.com']
    #start_urls = ['https://scholar.google.com/citations?view_op=view_org&hl=id&org=1388872056037598937']

    def start_requests(self):
        self.driver = webdriver.Chrome('/home/arham/chromedriver_linux64/chromedriver')         
        self.driver.get('http://scholar.google.com/citations?view_op=view_org&hl=id&org=1388872056037598937')

        sel = Selector(text=self.driver.page_source)    
        users = sel.xpath('//div[@id="gsc_sa_ccl"]/div[@class="gsc_1usr gs_scl"]/div[@class="gsc_oai"]/h3[@class="gsc_oai_name"]/a/@href').extract()
        
        for user in users:
            url = 'https://scholar.google.com' + user
            yield Request(url, callback=self.parse)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//button[@class="gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx"]')
                sleep(20)
                self.logger.info('Sleeping for 5 sec')
                next_page.click()

                sel = Selector(text=self.driver.page_source)    
                users = sel.xpath('//div[@id="gsc_sa_ccl"]/div[@class="gsc_1usr gs_scl"]/div[@class="gsc_oai"]/h3[@class="gsc_oai_name"]/a/@href').extract()
        
                for user in users:
                    url = 'https://scholar.google.com' + user
                    yield Request(url, callback=self.parse)
            
            except NoSuchElementException:
                self.logger.info('No more pages')
                self.driver.quit()
                break



    def parse(self, response):
        self.logger.info("Visited %s", response.url)
        self.driver = webdriver.Chrome('/home/arham/chromedriver_linux64/chromedriver')
        self.driver.get(response.url)
        page = self.driver.find_element_by_xpath('//button[@class="gs_btnPD gs_in_ib gs_btn_flat gs_btn_lrge gs_btn_lsu"]')
        button = page.is_enabled()

        if button is True:
            while button is True:
                page.click()
                sleep(2)
                button = page.is_enabled()
                if button is False:
                    #scrape here
                    for a in response.xpath('//*[@id="gsc_a_b"]/tr'):
                        nama = {
                            'Penelitian' : a.xpath('td[1]/a/text()').extract_first(),
                            'Jumlah' : a.xpath('td[2]/a/text()').extract_first(),
                        }
                        print(nama)
                    self.logger.info('Scraped')
                    self.driver.quit()
                    sleep(10)
                    break
        else:
            #scrape here
            for a in response.xpath('//*[@id="gsc_a_b"]/tr'):
                nama = {
                    'Penelitian' : a.xpath('td[1]/a/text()').extract_first(),
                    'Jumlah' : a.xpath('td[2]/a/text()').extract_first(),
                }
                print(nama)
                self.logger.info('Scraped')
                self.driver.quit()
                sleep(10)
            
