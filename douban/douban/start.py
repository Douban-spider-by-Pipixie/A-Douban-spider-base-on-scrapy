from scrapy import cmdline
from scrapy.crawler import CrawlerRunner
from utils.mysql_util import MysqlUtil
from spiders.book import BookSpider
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
import time
#ScrapyTest
# scrapy book_info where tag=科技
# cmdline.execute("scrapy crawl book -o books.json -a tag=科技".split())

# scrapy comment_info where bookID=6709783
# cmdline.execute("scrapy crawl comment -a bookID=6709783".split())


#DBTest
# scrapy book_info where tag=科技
# cmdline.execute("scrapy crawl book -a tag=科技".split())

# scrapy comment_info where bookID=6709783
# cmdline.execute("scrapy crawl comment -a bookID=6709783".split())

# scrapy tag
#cmdline.execute("scrapy crawl tag".split())

conn = MysqlUtil()
tags = conn.get_all('SELECT * FROM `test1.0`.`tag_Asyn`')
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    while True:
        for tag in tags:
            print('*********************')
            print('\t' + tag[0])
            print('*********************')
            yield runner.crawl(BookSpider,tag=tag[0])
            print('***************')
            print('SLEEPING FOR 6s')
            print('***************')
            time.sleep(6)
        reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished

