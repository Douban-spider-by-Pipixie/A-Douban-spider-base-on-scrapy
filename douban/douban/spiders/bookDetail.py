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
        'ITEM_PIPELINES': {'douban.pipelines.BookDetailAsynPipeline': 100}
    }

    def __init__(self, bookID=None, *args, **kwargs):
        super(BookDetailSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'https://book.douban.com/subject/' + bookID + '/']
        self.bookid = bookID

    def parse(self, response):
        sel = scrapy.Selector(response)
        try:
            item = BookDetail(
                book_introduct = sel.xpath('//div[@id="link-report"]//div[@class="intro"]').xpath("string(.)").extract()[0].replace('...(展开全部)','').replace('\n', '').replace('\t', ''),

                table = sel.xpath('//*[@id="dir_'+self.bookid+'_full"]').xpath('string(.)').extract()[0].replace('\n', '').replace('· · · · · ·     (收起)','').replace('\t', ''),

                author_introduct = sel.xpath('//div[@class="related_info"]//div[@class="intro"]').xpath('string(.)').extract()[0].replace('\n', '').replace('\t', ''),
                book_id = self.bookid
            )
            yield item
        except Exception as e:
            print(e)
            print("Yield BookDetail Error!")
            pass