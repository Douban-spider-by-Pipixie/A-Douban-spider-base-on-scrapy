# Scrapy
## V1.1 功能：
提供书本标签（tag）程序会自动爬取该标签下的全部书籍，可以转为Json格式；

### 运行脚本
在程序目录运行此命令：
```shell
scrapy crawl book -o items.json
```
### 选择要爬取的Tag 在[book.py](https://github.com/Douban-spider-by-Pipixie/Scrapy/blob/master/douban/douban/spiders/book.py)中设置
在spiders文件夹中的BookSpider类中更改（如科技类图书的爬取）：
```python
class BookSpider(scrapy.Spider):
    start_urls = [
        'https://book.douban.com/tag/科技'
    ]
    ···
```

### 目前爬取的字段 在[items.py](https://github.com/Douban-spider-by-Pipixie/Scrapy/blob/master/douban/douban/items.py)中设置
下一版本需要增加图片等信息：
```python
class BookItem(scrapy.Item):
    book_name = scrapy.Field()
    book_star = scrapy.Field()
    book_pl = scrapy.Field()
    book_author = scrapy.Field()
    book_publish = scrapy.Field()
    book_date = scrapy.Field()
    book_price = scrapy.Field()
```

### JSON样例 [样例](https://github.com/Douban-spider-by-Pipixie/Scrapy/blob/master/douban/items.json)
JSON中的UTF-8中文字符需要解码！
```json
[
{
"book_name":"解忧杂货店",
"book_star":"8.5",
"book_pl":"(622241人评价)",
"book_price":" 39.50元",
"book_date":" 2014-5 ",
"book_publish":" 南海出版公司 ",
"book_author":"[日] 东野圭吾 / 李盈春 "
},
{
"book_name":"白夜行",
"book_star":"9.1",
"book_pl":"(240275人评价)",
"book_price":" 39.50元",
"book_date":" 2013-1-1 ",
"book_publish":" 南海出版公司 ",
"book_author":"[日] 东野圭吾 / 刘姿君 "
},
···
```