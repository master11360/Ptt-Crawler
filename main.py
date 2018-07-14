def main(crawler_name):
    from scrapy import cmdline
    cmdline.execute(('scrapy crawl %s' % crawler_name).split())


if __name__ == '__main__':
    from test.spiders.crawler import PttCrawler

    main(PttCrawler.name)
