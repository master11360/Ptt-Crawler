# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Post(scrapy.Item):
    # define the fields for your item here like:
    # post list page
    author = scrapy.Field()
    push_num = scrapy.Field()
    mark = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    is_reply = scrapy.Field()
    post_id = scrapy.Field()
    author_nickname = scrapy.Field()
    time = scrapy.Field()

    is_deleted = scrapy.Field()  # TODO
    # post content page

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'%s [%s] %s' % (self['push_num'], self['category'], self['title'])
