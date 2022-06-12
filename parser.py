#-*- coding: UTF 8 -*-
import sys
import json
import time

import feedparser

from sqlalchemy.orm import mapper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, update, and_

Base = declarative_base()

class Source(object):
   """ 
   Class for parsing RSS
   """
   def __init__(self, config_links):
        self.links = [config_links[i] for i in config_links]
        self.news = []
        self.refresh()

   def refresh(self):
       self.news = []
       for n in self.links:
           data = feedparser.parse(n)
           self.news += [News(binascii.b2a_base64(i['title'].encode())\
                   .decode(),\
                         binascii.b2a_base64(i['link'].encode()).decode(),\
                                int(time.mktime(i['published_parsed'])))\
                                     for i in data['entries']]

