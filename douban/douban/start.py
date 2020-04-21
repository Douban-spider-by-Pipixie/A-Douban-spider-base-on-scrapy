from scrapy import cmdline
#ScrapyTest
# scrapy book_info where tag=科技
cmdline.execute("scrapy crawl book -o books.json -a tag=科技".split())

# scrapy comment_info where bookID=6709783
# cmdline.execute("scrapy crawl comment -a bookID=6709783".split())


#DBTest
# scrapy book_info where tag=科技
# cmdline.execute("scrapy crawl book -a tag=科技".split())

# scrapy comment_info where bookID=6709783
# cmdline.execute("scrapy crawl comment -a bookID=6709783".split())
