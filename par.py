import configparser
import logging

from lemma import Lemma 
#from trans import Trans

from news import News, Database, Source 


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
        #trans  = Trans()        
        lemma = Lemma()
        for n in news:
            if not self.db.find_link(n.link):
               # print(trans.translate_titles(n.title))
                logging.info( u'Detect news: %s' % n)
             #   self.db.add_news(n)
                print(n.summary)
            

def main():
    b = Bot()
    b.detect()



main()
