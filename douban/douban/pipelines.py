# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json


class DoubanPipeline(object):
    '''
    def __init__(self):
        self.file = codecs.open('result.json','wb','utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item))+'\n'
        self.file.write(line.encode('utf-8').decode("unicode_escape"))
        return item
    '''

    # def __init__(self):
    #     # 连接数据库
    #     self.connect = pymysql.connect(
    #         host='cdb-e0agigrr.gz.tencentcdb.com',  # 数据库地址
    #         port=10087,  # 数据库端口
    #         db='test1.0',  # 数据库名
    #         user='root',  # 数据库用户名
    #         passwd='16251425Zyq',  # 数据库密码
    #         charset='utf8',  # 编码方式
    #         use_unicode=True)
    #
    #     # 通过cursor执行增删查改
    #     self.cursor = self.connect.cursor()
    #
    # def open_spider(self, spider):
    #     print("爬虫开始....")
    #
    # def process_item(self, item, spider):
    #     self.insert_db(item)
    #     return item
    #
    # def insert_db(self, item):
    #     values = (
    #         item['book_name'],
    #         item['book_star'],
    #         item['book_pl'],
    #         item['book_author'],
    #         item['book_publish'],
    #         item['book_date'],
    #         item['book_price']
    #     )
    #     try:
    #         sql = 'INSERT INTO book VALUES(%s,%s,%s,%s,%s,%s,%s)'
    #         self.cursor.execute(sql, values)
    #         self.connect.commit()
    #         print("Insert finished")
    #     except:
    #         print("Insert to DB failed")
    #         self.connect.commit()
    #         self.connect.close()
    #
    # def close_spider(self, spoder):
    #     self.connect.commit()
    #     self.connect.close()
    #     print("爬虫结束....")
