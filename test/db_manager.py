from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    post_id = Column(String)
    title = Column(String)
    category = Column(String)
    author = Column(String)
    push_num = Column(String)
    mark = Column(String)
    url = Column(String)
    is_reply = Column(Integer)
    time = Column(String)
    content = Column(String)

    def __init__(self, **argd):
        super(Post, self).__init__()
        self.post_id = argd.get('post_id', '')
        self.title = argd.get('title', '')
        self.category = argd.get('category', '')
        self.author = argd.get('author', '')
        self.push_num = argd.get('push_num', '')
        self.mark = argd.get('mark', '')
        self.url = argd.get('url', '')
        self.is_reply = argd.get('is_reply', '')
        self.time = argd.get('time', '')
        self.content = argd.get('content', '')
