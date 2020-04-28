import codecs
import json

import pymysql
from twisted.enterprise import adbapi
import pymysql.cursors

import traceback
from DBUtils.PooledDB import PooledDB
from scrapy.utils.project import get_project_settings

class MysqlAsyncUtil(object):
    __dbpool = None

    def __init__(self):
        self.__dbpool = get_conn()


    def get_conn(self):
        if MysqlAsyncUtil.__dbpool is None:
            settings = get_project_settings()
            config = dict(
                host=settings.get('MYSQL_HOST'),
                port=settings.get('MYSQL_PORT'),
                db=settings.get('MYSQL_DATABASE'),
                user=settings.get('MYSQL_USER'),
                passwd=settings.get('MYSQL_PASSWORD'),
                charset=settings.get('MYSQL_CHARSET'),
                use_unicode=True,
                cursorclass=pymysql.cursors.DictCursor
            )
            dbpool = adbapi.ConnectionPool('pymysql',**config)
            return dbpool
