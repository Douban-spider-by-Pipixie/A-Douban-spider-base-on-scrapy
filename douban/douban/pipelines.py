# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings
import pymysql.cursors


# 图书信息异步管道
class BookItemAsynPipeline(object):
    def __init__(self, dbpool):
        settings = get_project_settings()
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 数据库建立连接
        adbparams = dict(
            host=settings.get('MYSQL_HOST'),  # 数据库地址
            port=settings.get('MYSQL_PORT'),  # 数据库端口
            db=settings.get('MYSQL_DATABASE'),  # 数据库名
            user=settings.get('MYSQL_USER'),  # 数据库用户名
            passwd=settings.get('MYSQL_PASSWORD'),  # 数据库密码
            charset=settings.get('MYSQL_CHARSET'),  # 编码方式
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
            print("BookItem Insert to DB failed")
            print(failure)


# 评论信息异步管道
class CommentItemAsynPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 数据库建立连接
        adbparams = dict(
            host=settings.get('MYSQL_HOST'),  # 数据库地址
            port=settings.get('MYSQL_PORT'),  # 数据库端口
            db=settings.get('MYSQL_DATABASE'),  # 数据库名
            user=settings.get('MYSQL_USER'),  # 数据库用户名
            passwd=settings.get('MYSQL_PASSWORD'),  # 数据库密码
            charset=settings.get('MYSQL_CHARSET'),  # 编码方式
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
            item['book_id'],
            item['comment_user'],
            item['comment_date'],
            item['comment'],
            item['comment_useful'],
            item['comment_star'],
        )
        sql = 'INSERT INTO commenttable_Asyn VALUES(%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, comment_values)

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print("CommentItem Insert to DB failed")
            print(failure)


# 标签信息异步管道
class TagItemAsynPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 数据库建立连接
        adbparams = dict(
            host=settings.get('MYSQL_HOST'),  # 数据库地址
            port=settings.get('MYSQL_PORT'),  # 数据库端口
            db=settings.get('MYSQL_DATABASE'),  # 数据库名
            user=settings.get('MYSQL_USER'),  # 数据库用户名
            passwd=settings.get('MYSQL_PASSWORD'),  # 数据库密码
            charset=settings.get('MYSQL_CHARSET'),  # 编码方式
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
            print("TagItem Insert to DB failed")
            print(failure)


# 图书对应标签信息异步管道
class BookTagsAsynPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 数据库建立连接
        adbparams = dict(
            host=settings.get('MYSQL_HOST'),  # 数据库地址
            port=settings.get('MYSQL_PORT'),  # 数据库端口
            db=settings.get('MYSQL_DATABASE'),  # 数据库名
            user=settings.get('MYSQL_USER'),  # 数据库用户名
            passwd=settings.get('MYSQL_PASSWORD'),  # 数据库密码
            charset=settings.get('MYSQL_CHARSET'),  # 编码方式
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
        book_tagItem = (
            item['book_id'],
            item['book_tag']
        )
        sql = 'INSERT INTO book_tag VALUES(%s,%s)'
        cursor.execute(sql, book_tagItem)

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print("BookTags Insert to DB failed")
            print(failure)

# 评论信息异步管道
class BookDetailAsynPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 数据库建立连接
        adbparams = dict(
            host=settings.get('MYSQL_HOST'),  # 数据库地址
            port=settings.get('MYSQL_PORT'),  # 数据库端口
            db=settings.get('MYSQL_DATABASE'),  # 数据库名
            user=settings.get('MYSQL_USER'),  # 数据库用户名
            passwd=settings.get('MYSQL_PASSWORD'),  # 数据库密码
            charset=settings.get('MYSQL_CHARSET'),  # 编码方式
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
            item['book_id'],
            item['book_introduct'],
            item['author_introduct'],
            item['table']
        )
        sql = 'INSERT INTO book_detail VALUES(%s,%s,%s,%s)'
        cursor.execute(sql, comment_values)

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print("BookDetail Insert to DB failed")
            print(failure)