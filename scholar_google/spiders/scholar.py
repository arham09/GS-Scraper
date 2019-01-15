# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Spider
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
from scrapy.http import Request

from twisted.internet.error import ConnectionRefusedError

class ScholarSpider(Spider):
    name = 'scholar'
    allowed_domains = ['scholar.google.com']
    #start_urls = ['https://scholar.google.com/citations?view_op=view_org&hl=id&org=1388872056037598937']

    def start_requests(self):
        self.driver = webdriver.Chrome('/home/arham/chromedriver_linux64/chromedriver')         
        self.driver.get('https://scholar.google.com/citations?view_op=view_org&hl=id&org=1388872056037598937')

        sel = Selector(text=self.driver.page_source)    
        users = sel.xpath('//div[@id="gsc_sa_ccl"]/div[@class="gsc_1usr gs_scl"]/div[@class="gsc_oai"]/h3[@class="gsc_oai_name"]/a/@href').extract()
        
        for user in users:
            url = 'https://scholar.google.com' + user
            yield Request(url, callback=self.parse)

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
                    yield Request(url, callback=self.parse)
                    sleep(2)
            else:
                self.logger.info("No More Pages")
                break
            
    def parse(self, response):
        self.logger.info("Visited %s", response.url)
        # self.driver = webdriver.Chrome('/home/arham/chromedriver_linux64/chromedriver')
        # self.driver.get(response.url)
        page = self.driver.find_element_by_xpath('//button[@class="gs_btnPD gs_in_ib gs_btn_flat gs_btn_lrge gs_btn_lsu"]')
        button = page.is_enabled()

        if button is True:
            while button is True:
                page.click()
                sleep(2)
                button = page.is_enabled()
                if button is False:
                    #scrape here
                    selector = Selector(text=self.driver.page_source)
                    nama = selector.xpath('//*[@id="gsc_prf_in"]/text()').extract_first()    
                    table = selector.xpath('//*[@id="gsc_a_b"]/tr')
                    for element in table:                                                                                              
                        penelitian = element.xpath('td[1]/a/text()').extract_first()
                        jumlah = element.xpath('td[2]/a/text()').extract_first()
                        
                        if jumlah is None:              
                            jumlah = 0
                        
                        # print(penelitian)
                        # print(jumlah)
                        yield {
                            "Nama" : nama,
                            "Judul" : penelitian,
                            "Jumlah" : jumlah
                        }
    
                    self.logger.info('Scraped')
                    self.driver.quit()
                    sleep(2)
                    break
        else:
            #scrape here
            selector = Selector(text=self.driver.page_source)
            nama = selector.xpath('//*[@id="gsc_prf_in"]/text()').extract_first()                        
            table = selector.xpath('//*[@id="gsc_a_b"]/tr')
            for element in table:                                                                                              
                penelitian = element.xpath('td[1]/a/text()').extract_first()
                jumlah = element.xpath('td[2]/a/text()').extract_first()
                        
                if jumlah is None:              
                    jumlah = 0

                # print(penelitian)
                # print(jumlah)
                yield {
                    "Nama" : nama,
                    "Judul" : penelitian,
                    "Jumlah" : jumlah
                }

            self.logger.info('Scraped')
            self.driver.quit()
            sleep(2)
                    