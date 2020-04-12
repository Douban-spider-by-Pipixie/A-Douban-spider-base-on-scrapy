# Scrapy
## V1.1 功能：
提供书本标签（tag）程序会自动爬取该标签下的全部书籍，可以转为Json格式；

### 运行脚本
在程序目录运行此命令：
```Shell
scrapy crawl book -o items.json
```
### 选择要爬取的Tag
在spiders文件夹中的BookSpider类中更改（如科技类图书的爬取）：
```python
class BookSpider(scrapy.Spider):
    start_urls = [
        'https://book.douban.com/tag/科技'
    ]
    ···
```