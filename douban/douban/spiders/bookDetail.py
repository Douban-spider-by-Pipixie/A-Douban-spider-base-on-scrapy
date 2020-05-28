import scrapy
import re
import sys
sys.path.append("..")
from items import BookDetail
from bs4 import BeautifulSoup


class BookDetailSpider(scrapy.Spider):
    name = 'bookDetail'
    bookid = ''
    '''
    custom_settings = {
        'ITEM_PIPELINES': {'douban.pipelines.BookDetailAsynAsynPipeline': 300}
    }
    '''

    def __init__(self, bookID=None, *args, **kwargs):
        super(BookDetailSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'https://book.douban.com/subject/' + bookID + '/']
        self.bookid = bookID

    def parse(self, response):
        sel = scrapy.Selector(response)
        try:
            item = BookDetail(
                book_introduct = sel.xpath('//div[@id="link-report"]/span[@class="short"]/div[@class="intro"]').xpath("string(.)").extract()[0].replace('...(展开全部)','').replace('\n', ''),
                table = sel.xpath('//*[@id="dir_'+self.bookid+'_full"]').xpath('string(.)').extract()[0].replace('\n', '').replace('· · · · · ·     (收起)',''),
                author_introduct = sel.xpath('//div[@class="related_info"]/div[@class="indent "]/div/div[@class="intro"]').xpath('string(.)').extract()[0].replace('\n', ''),
                book_id = self.bookid
            )
            yield item
        except Exception as e:
            print(e)
            print("Yield BookDetail Error!")
            pass