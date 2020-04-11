# -*- coding: utf-8 -*-
import scrapy
import re
from douban.items import BookItem
from bs4 import BeautifulSoup


class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = [
        'https://book.douban.com/tag/日本文学'
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        book_list = sel.css('#subject_list > ul > li')
        for book in book_list:
            try:
                pub = book.xpath('div[@class="info"]/div[@class="pub"]/text()').extract()[0].strip().split('/')
                #print(pub)
                item = BookItem(
                    book_name = book.xpath('div[@class="info"]/h2/a/text()').extract()[0].strip(),
                    book_star = book.xpath("div[@class='info']/div[2]/span[@class='rating_nums']/text()").extract()[
                    0].strip(),
                    book_pl = book.xpath("div[@class='info']/div[2]/span[@class='pl']/text()").extract()[0].strip(),
                    book_price = pub.pop(),
                    book_date = pub.pop(),
                    book_publish = pub.pop(),
                    book_author = '/'.join(pub)
                )
                yield item
            except Exception as e:
                print(e+"\n")
                print("Yield item error!")
                pass
        try:
            nextPage = sel.xpath('//div[@id="subject_list"]/div[@class="paginator"]/span[@class="next"]/a/@href').extract()[0].strip()
            if nextPage:
                next_url = 'https://book.douban.com'+nextPage
                yield scrapy.http.Request(next_url,callback=self.parse)
        except:
            pass

'''
    def parse_details(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        #Get Title
        try:
            bookName,bookUrl = self.extract_title(soup)
            if bookName is None:
                raise Exception('No Book for ' + response.url)
            print(bookName.strip()+bookUrl)
        except Exception as e:
            self.logger.error(str(e))

    def extract_title(self, soup):
        selectors = ['h2']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                bookName = soup.select(selector)[0].text.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                
                return bookName,url
'''
