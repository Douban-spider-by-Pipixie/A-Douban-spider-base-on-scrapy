from scrapy import cmdline
from scrapy.crawler import CrawlerRunner
from utils.mysql_util import MysqlUtil
from spiders.book import BookSpider
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
tags = conn.get_all('SELECT * FROM `test1.0`.`tag_Asyn`')
print(tags)
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    while True:
        for tag in tags:
            print('*********************')
            print('\t\a' + tag[0])
            print('*********************')

            yield runner.crawl(BookSpider,tag=tag[0])

            print('->'+ tag[0]+' FINISH' +'')
            print('\t->SLEEPING FOR 6s')
            print('')
            time.sleep(1)
            print('->'+ tag[0]+' FINISH' +'')
            print('\t->SLEEPING FOR 5s')
            print('')
            time.sleep(1)
            print('->'+ tag[0]+' FINISH' +'')
            print('\t->SLEEPING FOR 4s')
            print('')
            time.sleep(1)
            print('->'+ tag[0]+' FINISH' +'')
            print('\t->SLEEPING FOR 3s')
            print('')
            time.sleep(1)
            print('->'+ tag[0]+' FINISH' +'')
            print('\t->SLEEPING FOR 2s')
            print('')
            time.sleep(1)
            print('->'+ tag[0]+' FINISH' +'')
            print('\t->SLEEPING FOR 1s')
            print('')
            time.sleep(1)
        reactor.stop()

crawl()
#阻塞
reactor.run()
