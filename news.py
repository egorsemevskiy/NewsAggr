import sqlite3
import feedparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, update, and_

Base = declarative_base()

class News(Base):
    """
    Класс описыавющий новости.
    Так же взаимодействует с Базой
    """
    """
    Описание таблицы для sqlite3
    """
    __tablename__ = "news"
    id  = Column(Integer, primary_key=True)
    title = Column(String) 
    link = Column(String)
    # summary не работает на нескольких ресурсах,
    #TODO надо исправить
    #summary = Column(String)

    published = Column(Integer)

    
    def __init__(self, title, link, published):
        self.title = title
        self.link = link
        self.published = published
        #self.summary = summary
        
    """
    Текстовое представление класса 
    """
    def __repr__(self):
        return f"News:{self.title}, Link:{self.link}, Pub:{self.published}"

    """
    Ключи для сравнения записей
    """
    def _keys(self):
        return (self.title, self.link)

    """
    Сравнение происходит по ключам, то есть по заголовку
    и линку 
    """
    def __eq__(self, other):
        return self._keys() == other._keys()

    """
    ключи хешируются
    """
    def __hash__(self):
        return hash(self._keys())

class Database:

    def __init__(self, obj):
        engine = create_engine(obj, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_news(self, news):
        self.session.add(news)
        self.session.commit()
    
    def find_link(self,link):
        if self.session.query(News).filter_by(link = link).first(): return True
        else: return False 

class Source(object):

    def __init__(self, config_links):
        self.links = [config_links[i] for i in config_links]
        self.news = []
        self.refresh()

    def refresh(self):
        self.news = []
        for i in self.links:
            feedparser.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0i'
            data = feedparser.parse(i)
            if data.status == 200:
                print("All right")
                self.news += [News(i.title,i.link,i.published)\
                    for i in data['entries']]
            else:
                print(f'Some error - {data.status}')
