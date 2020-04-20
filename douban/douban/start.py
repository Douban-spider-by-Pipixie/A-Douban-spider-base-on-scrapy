from scrapy import cmdline

# use cmd in here
cmdline.execute("scrapy crawl book -o books.json -a tag=科技".split())
