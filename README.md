# Scrapy
## V1.2 功能：
1. 提供书本标签（tag）程序会自动爬取该标签下的全部书籍，可以转为Json格式
2. 提供书本的ID，程序会爬取该书本的全部评论，可以转为Json格式

### 运行脚本
1. 爬取书本
在程序目录运行此命令：
```shell
scrapy crawl book -o books.json
```
1. 爬取评论
在程序目录运行此命令：
```shell
scrapy crawl comment -o comments.json
```

### 选择要爬取的Tag/BookID 在[book.py](https://github.com/Douban-spider-by-Pipixie/Scrapy/blob/master/douban/douban/spiders/book.py) 或者 [comment.py](https://github.com/Douban-spider-by-Pipixie/Scrapy/blob/master/douban/douban/spiders/comment.py)中设置
在spiders文件夹中的BookSpider类中更改（如科技类图书的爬取）：
```python
class BookSpider(scrapy.Spider):
    start_urls = [
        'https://book.douban.com/tag/科技'
    ]
    ···
```
在spiders文件夹中的CommentSpider类中更改（如BookID = 6709783 图书的爬取）：
```python
class CommentSpider(scrapy.Spider):
    name = 'comment'
    start_urls = [
        'https://book.douban.com/subject/6709783/comments/'
    ]
    ···
```



### 目前爬取的字段 在[items.py](https://github.com/Douban-spider-by-Pipixie/Scrapy/blob/master/douban/douban/items.py)中设置
```python
class BookItem(scrapy.Item):
    book_id = scrapy.Field()
    book_img = scrapy.Field()
    book_name = scrapy.Field()
    book_star = scrapy.Field()
    book_commentCount = scrapy.Field()
    book_author = scrapy.Field()
    book_publish = scrapy.Field()
    book_date = scrapy.Field()
    book_price = scrapy.Field()

class Comment(scrapy.Item):
    comment_user = scrapy.Field()
    comment_time = scrapy.Field()
    comment = scrapy.Field()
    comment_useful = scrapy.Field()
    comment_star = scrapy.Field()
```

### JSON样例(图书) [样例](https://github.com/Douban-spider-by-Pipixie/Scrapy/blob/master/douban/books.json)
JSON中的UTF-8中文字符需要解码！
```json
[
    {
        "book_id": "26759508",
        "book_img": "https://img9.doubanio.com/view/subject/s/public/s28571694.jpg",
        "book_name": "硅谷钢铁侠",
        "book_star": "8.1",
        "book_commentCount": "7267",
        "book_price": " 68.00元",
        "book_date": " 2016-4 ",
        "book_publish": " 中信出版集团 ",
        "book_author": "[美] 阿什利·万斯 / 周恒星 "
    },
    {
        "book_id": "33424487",
        "book_img": "https://img3.doubanio.com/view/subject/s/public/s32332471.jpg",
        "book_name": "时间的秩序",
        "book_star": "8.9",
        "book_commentCount": "7635",
        "book_price": " 56.00元",
        "book_date": " 2019-6 ",
        "book_publish": " 湖南科学技术出版社 ",
        "book_author": "[意] 卡洛·罗韦利 / 杨光 "
    }
]
```

### JSON样例(评论) [样例](https://github.com/Douban-spider-by-Pipixie/Scrapy/blob/master/douban/comments.json)
JSON中的UTF-8中文字符需要解码！
```json
[
   {
        "comment_user": "和尚",
        "comment_time": "2019-01-01",
        "comment": "在吴晓波的书中，我们能看到对中国短暂的现代商业史中消逝公司的惋惜，实际上我们也常假设：某某公司若还存在会如何。但世间没有如果，这本书给了一个很独特的视角：“一个公司的死亡是对社会最后的一次贡献”。既然一个公司无法再适应，那能通过自身的消逝为后来者提供警示和腾出市场资源，伤害的是自己，但有利于整个社会。这个自由主义十足的观点，也适用于我们这个正在极度变化和充满竞争中社会的每个个体。",
        "comment_useful": "4",
        "comment_star": "力荐"
    },
    {
        "comment_user": "hiro",
        "comment_time": "2012-08-31",
        "comment": "生在这个时代最大的幸运就是可以看到商业和科学技术完美结合不断的改变这个世界的面貌，不断的改变我们的生活方式。   吴军博士不断的说能赶上科技发展的浪潮便不枉此生，每次读到这，心里都很不受用。",
        "comment_useful": "3",
        "comment_star": "力荐"
    },
    {
        "comment_user": "hushlight",
        "comment_time": "2014-03-03",
        "comment": "因为这个名字加畅销书属性，我以为是本夸夸其谈的成功学，所以到现在才看完。蛮有意思的IT史，文笔朴实生动。批评的声音多指此书结论过于简略，细节失之确凿，没有一手材料。我嚼着这书本来定位也不是商学院案例分析，几十块钱能让你知道以前不知道的东西，还想要什么啊",
        "comment_useful": "2",
        "comment_star": "推荐"
    }
]
```