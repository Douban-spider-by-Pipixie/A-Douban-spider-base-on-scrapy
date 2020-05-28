# Scrapy
### V1.0 功能 2020-3-15：
- 网上提供的示例程序作为参考

### V1.1 功能 2020-4-5：
- 提供书本标签（tag）程序会自动爬取该标签下的全部书籍，可以转为Json格式

### V1.2 功能 2020-4-18：
- 提供书本的ID，程序会爬取该书本的全部评论，可以转为Json格式
- 可以用 [管线](douban/douban/pipelines.py) 完成数据直接插入数据库的操作

### V1.2.1 功能 2020-4-20：
- 修正了 [BookSpider](douban/douban/spiders/book.py) 和 [CommentSpider](douban/douban/spiders/comment.py) 的构造方式，可以通过传入参数的方式指定爬取内容

### V1.2.2 功能 2020-4-20：
- 修正了生成Json时候的UTF-8编码错误
- 字段"comment_time" 改为 "comment_date"
  
### V1.2.3 功能 2020-4-24：
- 数据库的插入改为异步方法NIO，有效提升效率

### V1.3.3 功能 2020-4-25：
- 增加 [tag.py](douban/douban/spiders/tag.py) 可以爬取所有标签和热门标签

### V1.3.4 功能 2020-4-27
- 增加 [mysql_util.py](douban/douban/utils/mysql_util.py) 作为数据库连接池工具类
  - [pipelines.py](douban/douban/pipelines.py) 需要引入工具类重构
- 更新了 [start.py](douban/douban/start.py) 加入了自动爬虫功能，直接运行脚本即可

### V1.3.5 功能 2020-4-28
- 修复了项目层次结构的问题
- 废弃pipeline中所写的所有同步同步管道。
- 新增booktag管道，用于存储图书-标签对
- 修改pipeline中用于数据库连接的配置，同一从settings获取，避免后期修改时需要深入代码内部

### V1.4.5 功能 2020-5-28
- 新增了爬取书本详情的功能[bookDetail.py](douban/douban/spiders/bookDetail.py) , 传入bookID爬取书本简介、书本目录、书本作者简介

### 运行脚本

1. 爬取书本

在程序目录运行此命令（以爬取科技类图书为例）：

```bash
scrapy crawl book -o books.json -a tag=科技
```

2. 爬取评论

在程序目录运行此命令（以书本ID: 6709783 为例）：

```bash
scrapy crawl comment -o comments.json -a bookID=6709783
```

3. 爬取标签

在程序目录运行此命令（以书本ID: 6709783 为例）：

```bash
scrapy crawl tag -o tags.json
```

### 选择要爬取的 Tag / BookID 

爬取书本时，[BookSpider](douban/douban/spiders/book.py) 类要传入tag参数以构造该类爬取对应tag的数据：

```python
class BookSpider(scrapy.Spider):
    name = 'book'
    tag = ''

    def __init__(self, tag=None, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://book.douban.com/tag/' + tag]
        self.tag = tag
    ···
```
[BookSpider](douban/douban/spiders/book.py) 构造方法实例：
```python
from douban.items import BookItem
from scrapy.crawler import CrawlerProcess


process = CrawlerProcess()
process.crawl(BookItem(tag = '科技'))
process.start()
···
```

爬取书本时，[Comment](douban/douban/spiders/comment.py) 类要传入BookID参数以构造该类爬取对应BookID的数据：

```python
class CommentSpider(scrapy.Spider):
    name = 'comment'
    bookid = ''

    def __init__(self, bookID=None, *args, **kwargs):
        super(CommentSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'https://book.douban.com/subject/' + bookID + '/comments/']
        self.bookid = bookID
    ···
```

[Comment](douban/douban/spiders/comment.py) 构造方法实例：
```python
from douban.items import Comment
from scrapy.crawler import CrawlerProcess


process = CrawlerProcess()
process.crawl(Comment(bookID = '0000001'))
process.start()
···
```

### 目前爬取的字段 在 [items.py](https://github.com/Douban-spider-by-Pipixie/Scrapy/blob/master/douban/douban/items.py) 中设置

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

### JSON样例(标签) [样例](douban/tags.json)
```json
[
    {"tag_name": "交互", "tag_isHot": false},
    {"tag_name": "通信", "tag_isHot": false},
    {"tag_name": "UE", "tag_isHot": false},
    {"tag_name": "神经网络", "tag_isHot": false},
    {"tag_name": "UCD", "tag_isHot": false},
    {"tag_name": "程序", "tag_isHot": false},
    {"tag_name": "小说", "tag_isHot": true},
    {"tag_name": "历史", "tag_isHot": true},
    {"tag_name": "日本", "tag_isHot": true}
]
```
