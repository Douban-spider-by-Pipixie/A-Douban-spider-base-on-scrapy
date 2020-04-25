# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

import pymysql
from twisted.enterprise import adbapi
import pymysql.cursors


# 图书信息同步管道
class BookItemSynPipeline(object):
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
        print("BookItem spider start....")

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
        print("BookItem spider end....")


# 图书信息异步管道
class BookItemAsynPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 数据库建立连接
        adbparams = dict(
            host='cdb-e0agigrr.gz.tencentcdb.com',  # 数据库地址
            port=10087,  # 数据库端口
            db='test1.0',  # 数据库名
            user='root',  # 数据库用户名
            passwd='16251425Zyq',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常
        return item

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
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
        sql = 'INSERT INTO book_Asyn VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, book_values)

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print("Insert to DB failed")
            print(failure)


# 评论信息同步管道
class CommentItemSynPipeline(object):
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
        print("CommentItem spider start....")

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
        print("CommentItem spider end....")


# 评论信息异步管道
class CommentItemAsynPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 数据库建立连接
        adbparams = dict(
            host='cdb-e0agigrr.gz.tencentcdb.com',  # 数据库地址
            port=10087,  # 数据库端口
            db='test1.0',  # 数据库名
            user='root',  # 数据库用户名
            passwd='16251425Zyq',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常
        return item

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        comment_values = (
            item['comment_user'],
            item['comment_date'],
            item['comment'],
            item['comment_useful'],
            item['comment_star'],
        )
        sql = 'INSERT INTO commenttable_Asyn VALUES(%s,%s,%s,%s,%s)'
        cursor.execute(sql, comment_values)

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print("Insert to DB failed")
            print(failure)


# 评论信息异步管道
class TagItemSynPipeline(object):
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
        print("TagItem spider start....")

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        tag_values = (
            item['tag_name'],
            item['tag_isHot']
        )
        try:
            sql = 'REPLACE INTO tag VALUES(%s,%s)'
            self.cursor.execute(sql, tag_values)
            self.connect.commit()
            print("Insert one comment finished")
        except:
            print("Insert to DB failed")
            self.connect.commit()
            self.connect.close()

    def close_spider(self, spoder):
        self.connect.commit()
        self.connect.close()
        print("TagItem spider start....")


# 评论信息异步管道
class TagItemAsynPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 数据库建立连接
        adbparams = dict(
            host='cdb-e0agigrr.gz.tencentcdb.com',  # 数据库地址
            port=10087,  # 数据库端口
            db='test1.0',  # 数据库名
            user='root',  # 数据库用户名
            passwd='16251425Zyq',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常
        return item

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        tag_values = (
            item['tag_name'],
            item['tag_isHot']
        )
        sql = 'REPLACE INTO tag_Asyn VALUES(%s,%s)'
        cursor.execute(sql, tag_values)

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print("Insert to DB failed")
            print(failure)
