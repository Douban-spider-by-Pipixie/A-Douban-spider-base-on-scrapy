from scrapy import cmdline
from scrapy.crawler import CrawlerRunner
from utils.mysql_util import MysqlUtil
from spiders.book import BookSpider
from spiders.bookDetail import BookDetailSpider
from spiders.comment import CommentSpider
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
import time
import pymysql

#  ________  ___  ___  _________  ________     
# |\   __  \|\  \|\  \|\___   ___\\   __  \    
# \ \  \|\  \ \  \\\  \|___ \  \_\ \  \|\  \   
#  \ \   __  \ \  \\\  \   \ \  \ \ \  \\\  \  
#   \ \  \ \  \ \  \\\  \   \ \  \ \ \  \\\  \ 
#    \ \__\ \__\ \_______\   \ \__\ \ \_______\
#     \|__|\|__|\|_______|    \|__|  \|_______|

#  ________  ________  ________  ___       __   ___       _______   ________     
# |\   ____\|\   __  \|\   __  \|\  \     |\  \|\  \     |\  ___ \ |\   __  \    
# \ \  \___|\ \  \|\  \ \  \|\  \ \  \    \ \  \ \  \    \ \   __/|\ \  \|\  \   
#  \ \  \    \ \   _  _\ \   __  \ \  \  __\ \  \ \  \    \ \  \_|/_\ \   _  _\  
#   \ \  \____\ \  \\  \\ \  \ \  \ \  \|\__\_\  \ \  \____\ \  \_|\ \ \  \\  \| 
#    \ \_______\ \__\\ _\\ \__\ \__\ \____________\ \_______\ \_______\ \__\\ _\ 
#     \|_______|\|__|\|__|\|__|\|__|\|____________|\|_______|\|_______|\|__|\|__|

conn = MysqlUtil()
#tags = conn.get_all('SELECT * FROM `test1.0`.`tag_Asyn`')
ids = conn.get_all('SELECT `test1.0`.`book_Asyn`.`book_id` FROM `test1.0`.`book_Asyn` LEFT JOIN `test1.0`.`book_detail` ON `test1.0`.`book_Asyn`.`book_id` = `test1.0`.`book_detail`.`book_id` WHERE `book_introduct` IS NULL;')
print(ids)
#cids = conn.get_all(' SELECT `test1.0`.`book_Asyn`.`book_id` FROM `test1.0`.`book_Asyn` LEFT JOIN `commenttable_Asyn` cA on `book_Asyn`.`book_id` = cA.`book_id` WHERE `comment` IS NULL; ')
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    while True:
        for tag in tags:
            print('*********************')
            print('\t\a' + tag[0])
            print('*********************')

            yield runner.crawl(BookSpider,tag=tag[0])
        reactor.stop()

@defer.inlineCallbacks
def detail():
    while True:
        for ID in ids:
            print('*********************')
            print('\t\a' + ID[0])
            print('*********************')

            yield runner.crawl(BookDetailSpider,bookID=ID[0])

            time.sleep(1)

        reactor.stop()

@defer.inlineCallbacks
def comment():
    while True:
        for ID in cids:
            print('*********************')
            print('\t\a' + ID[0])
            print('*********************')

            yield runner.crawl(CommentSpider,bookID=ID[0])

        reactor.stop()

detail()
#comment()
reactor.run()
