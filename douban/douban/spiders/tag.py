import scrapy
import re
from douban.items import Tag
from bs4 import BeautifulSoup


class TagSpider(scrapy.Spider):
    name = 'tag'
    start_urls = [
        'https://book.douban.com/tag/'
    ]
    custom_settings = {
        # 'ITEM_PIPELINES': {'douban.pipelines.TagItemSynPipeline': 300},
        'ITEM_PIPELINES': {'douban.pipelines.TagItemAsynPipeline': 300}

    }

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        tag_list = soup.find_all('a', href=re.compile(r'/tag/.*'))
        for tag in tag_list:
            try:
                if (tag.text != '所有热门标签' and tag.text != '分类浏览' and response.url == 'https://book.douban.com/tag/'):
                    item = Tag(
                        tag_name=tag.text,
                        tag_isHot=0
                    )
                elif (
                        tag.text != '所有热门标签' and tag.text != '分类浏览' and response.url == 'https://book.douban.com/tag/?view=cloud'):
                    item = Tag(
                        tag_name=tag.text,
                        tag_isHot=1
                    )
                print(tag)
                yield item
            except Exception as e:
                print(e.args)
                print("Yield Tag Error!")
                pass

        yield scrapy.http.Request('https://book.douban.com/tag/?view=cloud', callback=self.parse)
