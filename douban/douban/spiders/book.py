# -*- coding: utf-8 -*-
import scrapy
import re
from douban.items import BookItem
from bs4 import BeautifulSoup


class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = [
        'https://book.douban.com/tag/\u79d1\u6280'
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        # //*[@id="subject_list"]/ul/li[1]
        book_list = sel.css('#subject_list > ul > li')
        for book in book_list:
            try:
                bookid = book.xpath('div[@class="info"]/h2/a/@href').extract()[0].strip().replace('https://book.douban.com/subject/','').replace('/','')
                pub = book.xpath('div[@class="info"]/div[@class="pub"]/text()').extract()[0].strip().split('/')
                #print(pub)
                item = BookItem(

                    book_id = bookid,
                    # //*[@id="subject_list"]/ul/li[1]/div[1]/a/img
                    book_img = book.xpath('div[@class="pic"]/a/img/@src').extract()[0].strip(),
                    # //*[@id="subject_list"]/ul/li[1]/div[2]/h2/a
                    # //*[@id="subject_list"]/ul/li[1]/div[2]/h2/a
                    book_name = book.xpath('div[@class="info"]/h2/a/text()').extract()[0].strip(),
                    # //*[@id="subject_list"]/ul/li[1]/div[2]/div[2]/span[2]
                    book_star = book.xpath("div[@class='info']/div[2]/span[@class='rating_nums']/text()").extract()[
                    0].strip(),
                    book_commentCount = book.xpath("div[@class='info']/div[2]/span[@class='pl']/text()").extract()[0].strip().replace("(","").replace("\u4eba\u8bc4\u4ef7)",""),
                    book_price = pub.pop(),
                    book_date = pub.pop(),
                    book_publish = pub.pop(),
                    book_author = '/'.join(pub)
                )
                yield item
            except Exception as e:
                print(e.args)
                print("Yield Book Error!")
                pass
        try:
            nextPage = sel.xpath('//div[@id="subject_list"]/div[@class="paginator"]/span[@class="next"]/a/@href').extract()[0].strip()
            if nextPage:
                next_url = 'https://book.douban.com'+nextPage
                yield scrapy.http.Request(next_url,callback=self.parse)
        except:
            pass