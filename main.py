def main(crawler_name):
    from scrapy import cmdline
    cmdline.execute(('scrapy crawl %s' % crawler_name).split())


if __name__ == '__main__':
    import win_unicode_console
    from scrapy_crawler.spiders.crawler import PttCrawler

    win_unicode_console.enable()
    main(PttCrawler.name)
