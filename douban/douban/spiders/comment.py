import scrapy
import re
from douban.items import Comment
from bs4 import BeautifulSoup


class CommentSpider(scrapy.Spider):
    name = 'comment'
    start_urls = [
        'https://book.douban.com/subject/6709783/comments/'
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        comment_list = sel.css('#comments > ul > li')
        for comment in comment_list:
            try:
                item = Comment(
                    # //*[@id="comments"]/ul/li[1]/div[2]/h3/span[2]/a
                    comment_user = comment.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/a/text()').extract()[0].strip(),
                    comment_time = comment.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span[2]/text()').extract()[0].strip(),
                    comment = comment.xpath('div[@class="comment"]/p/span/text()').extract()[0].strip(),
                    comment_useful = comment.xpath('div[@class="comment"]/h3/span[@class="comment-vote"]/span/text()').extract()[0].strip(),
                    comment_star = comment.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span[1]/@title').extract()[0].strip()
                )
                yield item
            except Exception as e:
                print(e.args)
                print("Yield Comment Error!")
                pass
        try:
            nextPage = sel.xpath('//*[@id="content"]/div/div[1]/div/div[3]/ul/li[3]/a/@href').extract()[0].strip()
            if nextPage:
                next_url = response.url + nextPage
                yield scrapy.http.Request(next_url,callback=self.parse)

        except Exception as e:
            print(e.args)
            pass