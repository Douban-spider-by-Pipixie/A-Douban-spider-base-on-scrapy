import scrapy
import re
import sys
sys.path.append("..")
from items import BookDetail
from bs4 import BeautifulSoup


class BookDetailSpider(scrapy.Spider):
    name = 'bookDetail'
    bookid = ''

    custom_settings = {
        'ITEM_PIPELINES': {'douban.pipelines.BookDetailAsynPipeline': 300}
    }

    def __init__(self, bookID=None, *args, **kwargs):
        super(BookDetailSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'https://book.douban.com/subject/' + bookID + '/']
        self.bookid = bookID

    def parse(self, response):
        sel = scrapy.Selector(response)


        try:
            bookIntroduct = sel.xpath('//div[@id="link-report"]//*[@class="all hidden"]//div[@class="intro"]').xpath("string(.)").extract()[0].replace('\t', '')
        except Exception as e:
            print("book_introduct NO ADD-ON!")
            bookIntroduct = sel.xpath('//div[@id="link-report"]//div[@class="intro"]').xpath("string(.)").extract()[0].replace('\t', '')

        try:
            authorIntroduct = sel.xpath('//div[@class="related_info"]//span[@class="all hidden "]/div[@class="intro"]').xpath('string(.)').extract()[0].replace('\t', '')
        except Exception as e:
            print("author_introduct NO ADD-ON!")
            authorIntroduct = sel.xpath('//div[@class="related_info"]/div[@class="indent "]//div[@class="intro"]').xpath('string(.)').extract()[0].replace('\t', ''),


        try:
            item = BookDetail(
                book_introduct = bookIntroduct,

                table = sel.xpath('//*[@id="dir_'+self.bookid+'_full"]').xpath('string(.)').extract()[0].replace('· · · · · ·     (收起)','').replace('\t', ''),

                author_introduct = authorIntroduct,
                book_id = self.bookid
            )
            yield item
            return
        except Exception as e:
            print("Yield Book Detail Error!")
            pass