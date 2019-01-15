# -*- coding: utf-8 -*-
from scrapy import Spider
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
from scrapy.http import Request


class ProfilSpider(Spider):
    name = 'profil'
    allowed_domains = ['scholar.google.co.id']
    start_urls = ['https://scholar.google.co.id/citations?user=oRWiRGQAAAAJ/']

    # def start_requests(self):
    #     self.driver = webdriver.Chrome('/home/arham/chromedriver_linux64/chromedriver')
    #     self.driver.get('https://scholar.google.co.id/citations?user=oRWiRGQAAAAJ/')
    #     url = 'https://scholar.google.co.id/citations?user=oRWiRGQAAAAJ/'   
    #     # page = self.driver.find_element_by_xpath('//button[@class="gs_btnPD gs_in_ib gs_btn_flat gs_btn_lrge gs_btn_lsu"]')
    #     # button = page.is_enabled()

    #     yield Request(url, 
    #                     meta={
    #                         'dont_redirect': True
    #                     },
    #                     callback=self.parse)

        # if button is True:
        #     while button is True:
        #         page.click()
        #         button = page.is_enabled()
        #         if button is False:
        #             #scrape here
        #             selector = Selector(text=self.driver.page_source)
        #             nama = selector.xpath('//*[@id="gsc_prf_in"]/text()').extract_first()    
        #             table = selector.xpath('//*[@id="gsc_a_b"]/tr')
        #             for element in table:                                                                                              
        #                 penelitian = element.xpath('td[1]/a/text()').extract_first()
        #                 jumlah = element.xpath('td[2]/a/text()').extract_first()
                        
        #                 if jumlah is None:              
        #                     jumlah = 0
                        
        #                 # print(penelitian)
        #                 # print(jumlah)
        #                 yield {
        #                     "Nama" : nama,
        #                     "Judul" : penelitian,
        #                     "Jumlah" : jumlah
        #                 }
    
        #             self.logger.info('Scraped')
        #             self.driver.quit()
        #             break
        # else:
        #     #scrape here
        #     selector = Selector(text=self.driver.page_source)
        #     nama = selector.xpath('//*[@id="gsc_prf_in"]/text()').extract_first()                        
        #     table = selector.xpath('//*[@id="gsc_a_b"]/tr')
        #     for element in table:                                                                                              
        #         penelitian = element.xpath('td[1]/a/text()').extract_first()
        #         jumlah = element.xpath('td[2]/a/text()').extract_first()
                        
        #         if jumlah is None:              
        #             jumlah = 0

        #         # print(penelitian)
        #         # print(jumlah)
        #         yield {
        #             "Nama" : nama,
        #             "Judul" : penelitian,
        #             "Jumlah" : jumlah
        #         }

        #     self.logger.info('Scraped')
        #     self.driver.quit()
    
    def parse(self, response):
        self.logger.info("Visited %s", self.start_urls)
        self.driver = webdriver.Chrome('/home/arham/chromedriver_linux64/chromedriver')
        self.driver.get(response.url)
        page = self.driver.find_element_by_xpath('//button[@class="gs_btnPD gs_in_ib gs_btn_flat gs_btn_lrge gs_btn_lsu"]')
        button = page.is_enabled()

        if button is True:
            while button is True:
                page.click()
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
            
