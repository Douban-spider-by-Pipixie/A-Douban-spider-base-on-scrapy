# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

import pymysql


class BookItemPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='cdb-e0agigrr.gz.tencentcdb.com',  # 数据库地址
            port=10087,  # 数据库端口
            db='test1.0',  # 数据库名
            user='root',  # 数据库用户名
            passwd='16251425Zyq',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def open_spider(self, spider):
        print("爬虫开始....")

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        book_values = (
            item['book_id'],
            item['book_img'],
            item['book_name'],
            item['book_star'],
            item['book_commentCount'],
            item['book_author'],
            item['book_publish'],
            item['book_date'],
            item['book_price']
        )
        try:
            sql = 'INSERT INTO book VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql, book_values)
            self.connect.commit()
            print("Insert finished")
        except:
            print("Insert to DB failed")
            self.connect.commit()
            self.connect.close()

    def close_spider(self, spoder):
        self.connect.commit()
        self.connect.close()
        print("爬虫结束....")


class CommentItemPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='cdb-e0agigrr.gz.tencentcdb.com',  # 数据库地址
            port=10087,  # 数据库端口
            db='test1.0',  # 数据库名
            user='root',  # 数据库用户名
            passwd='16251425Zyq',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def open_spider(self, spider):
        print("爬虫开始....")

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        comment_values = (
            item['comment_user'],
            item['comment_date'],
            item['comment'],
            item['comment_useful'],
            item['comment_star'],
        )
        try:
            sql = 'INSERT INTO commenttable VALUES(%s,%s,%s,%s,%s)'
            self.cursor.execute(sql, comment_values)
            self.connect.commit()
            print("Insert one comment finished")
        except:
            print("Insert to DB failed")
            self.connect.commit()
            self.connect.close()

    def close_spider(self, spoder):
        self.connect.commit()
        self.connect.close()
        print("爬虫结束....")
