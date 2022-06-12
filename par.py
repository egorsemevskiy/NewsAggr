import sqlite3
import feedparser
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, update, and_
from datetime import datetime


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
    publish = Column(Integer)

    def __init__(self, title, link, publish):
        self.title = title
        self.link = link
        self.publish = publish
        
    def __repr__(self):
        return f"News:{self.title}, Link:{self.link}, Pub:{self.publish}"

    def _keys(self):
        return (self.text, self.link)

    def __eq__(self, other):
        return self._keys() == other._keys()

    def __hash__(self):
        return hash(self._keys())

def sourse(link_list):
    news = []
    for l in link_list:
        data = feedparser.parse(l)
        for entry in data.entries:
            print( News(entry.title, entry.link, entry.published))
            
            ##print(entry.keys())


def main():
    sourse(["http://tass.ru/rss/v2.xml"])

main()
