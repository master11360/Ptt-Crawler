# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from bs4 import NavigableString
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
import os
from test.db_manager import Post
from sqlalchemy import exists
import datetime

PTT_DOMAIN = 'https://www.ptt.cc'
PTT_MOVIE_BOARD = PTT_DOMAIN + '/bbs/movie/index.html'
CATEGORY_ANNOUNCEMENT = u'公告'


class PttCrawler(scrapy.Spider):
    name = 'ptt_movie'
    start_urls = [PTT_MOVIE_BOARD]

    def __init__(self):
        super(PttCrawler, self).__init__()
        self.dic_post = {}
        self.db = create_engine('sqlite:///%s' % '../ptt.db')
        session_maker = sessionmaker(bind=self.db)
        self.db_session = session_maker()

    def parse(self, response):
        res = BeautifulSoup(response.body, "lxml")
        for post_content in res.select('.r-ent'):
            author = self.parse_author(post_content)
            if author == '-':
                # TODO: deal with 'is_deleted'
                # if no author, means the post_content is deleted
                continue

            post = Post()
            post.author = author
            post.push_num = self.parse_push_num(post_content)
            post.mark = self.parse_mark(post_content)
            full_title = self.parse_full_title(post_content)
            post.category = self.parse_category(full_title)
            post.title = self.parse_title(full_title)
            post.is_reply = self.parse_is_reply(full_title)
            post.url = self.parse_url(post_content)
            post.post_id = self.parse_post_id(post.url)
            if post.url:
                self.dic_post[post.post_id] = post
                time.sleep(0.1)
                yield scrapy.Request(post.url, self.parse_post_detail, meta={'post_id': post.post_id,
                                                                             'author': post.author,
                                                                             'db_row': post})
            print post

            is_post_exist_in_db = self.db_session.query(
                exists().where(Post.post_id == post.post_id)).scalar()
            if is_post_exist_in_db:
                self.db_session.query().filter(Post == post.post_id) \
                    .update({Post.push_num: post.push_num})
            else:
                self.db_session.add(post)
            # self.db_session.add(db_post)
            self.db_session.commit()

        # previous page
        # div_btn_group_paging = res.select('.btn-group-paging.btn-group')[0]
        # a_prev_page = div_btn_group_paging.select('a')[1]
        # if a_prev_page['href']:
        #     time.sleep(0.1)
        #     yield scrapy.Request(PTT_DOMAIN + a_prev_page['href'], self.parse)

    def parse_post_detail(self, response):
        post_id = response.meta['post_id']
        if post_id in self.dic_post:
            res = BeautifulSoup(response.body, "lxml")
            author_nickname = self.parse_author_nickname(res, response.meta['author'])
            time = self.parse_time(res)
            content = self.parse_content(res)
            is_post_exist_in_db = self.db_session.query(
                exists().where(Post.post_id == post_id)).scalar()
            if is_post_exist_in_db:
                db_post = response.meta['db_row']
                db_post.time = time
                db_post.content = content
                self.db_session.commit()
            del self.dic_post[post_id]

    def parse_author(self, content):
        return content.select('.author')[0].text

    def parse_push_num(self, content):
        nrec = content.select('.nrec > span')
        return nrec[0].text if nrec else 0

    def parse_mark(self, content):
        mark = content.select('.mark > span')
        return mark[0].text if mark else ''

    def parse_full_title(self, content):
        a_title = content.select('.title > a')
        if a_title:
            return a_title[0].text
        else:
            return content.select('.title')[0].text

    def parse_category(self, full_title):
        try:
            tmp = full_title.split(']')
            return tmp[0].replace('[', '').replace('Re:', '').strip()
        # TODO: raise exception
        except:
            return ''

    def parse_title(self, full_title):
        try:
            tmp = full_title.split(']')
            return tmp[1].strip()
        # TODO: raise exception
        except:
            return ''

    def parse_is_reply(self, full_title):
        return full_title.startswith('Re:')

    def parse_url(self, content):
        a_title = content.select('.title > a')
        if a_title:
            return PTT_DOMAIN + a_title[0]['href'] if hasattr(a_title[0], 'href') else ''
        else:
            return ''

    def parse_post_id(self, url):
        _, id_str = os.path.split(url)
        return os.path.splitext(id_str)[0]

    def parse_author_nickname(self, content, author):
        try:
            author_and_nickname = content.select('.article-meta-value')[0].text
            return author_and_nickname.replace(author, '').strip()[1:-1]
        # TODO: raise exception
        except:
            return ''

    def parse_time(self, content):
        try:
            time = content.select('span.article-meta-value')[-1].text
            format_time = datetime.datetime.strptime(time, '%a %b %d %H:%M:%S %Y')
            return format_time.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return ''

    def parse_content(self, content):
        div_content = content.select('div#main-content')[0]
        str = [tmp for tmp in div_content.contents if isinstance(tmp, NavigableString)][0]
        # str = None
        # for tmp in div_content.contents:
        #     if isinstance(tmp, NavigableString):
        #         str = tmp
        #         break
        return str