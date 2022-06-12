import feedparser
import configparser
import logging

import sqlite3
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
    __tablename__ = "news"
    id  = Column(Integer, primary_key=True)
    title = Column(String) 
    link = Column(String)
    published = Column(Integer)

    def __init__(self, title, link, published):
        self.title = title
        self.link = link
        self.published = published
        
    def __repr__(self):
        return f"News:{self.title}, Link:{self.link}, Pub:{self.published}"

    def _keys(self):
        return (self.text, self.link)

    def __eq__(self, other):
        return self._keys() == other._keys()

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
            data = feedparser.parse(i)
            self.news += [News(i.title, i.link, i.published) \
                    for i in data['entries']]






class Bot:
    """
    Основной класс программмы
    """
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config')
        log_file = config['Export_params']['log_file']
        self.pub_pause = int(config['Export_params']['pub_pause'])
        self.delay_between_messages = int\
                (config['Export_params']['delay_between_messages'])
        logging.basicConfig\
                (filename=config['Export_params']['log_file'],\
               encoding='utf-8', level=logging.INFO)
        self.db = Database(config['Database']['Path'])
        self.src = Source(config['RSS'])
    
    def detect(self):
        self.src.refresh()
        news = self.src.news
        news.reverse()

        for n in news:
            if not self.db.find_link(n.link):
                logging.info( u'Detect news: %s' % n)
                self.db.add_news(n)

def main():
    #sourse(["http://tass.ru/rss/v2.xml"])
    #create_connection('news.db')
    b = Bot()
    b.detect()
main()
