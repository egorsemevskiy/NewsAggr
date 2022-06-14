import configparser
import logging

from lemma import Lemma 

from news import News, Database, Source 


class Bot:
    """
    Основной класс программмы
    """
    def __init__(self):
        """
        Создается обьект парсера конфигов
        Все конфиги лежат в файле ./config
        Там же хранится список RSS каналов, что мы парсим
        """
        config = configparser.ConfigParser()
        config.read('./config')
        log_file = config['Export_params']['log_file']
        """
        Эти две переменные для постинга. Пока не используются
        """
        self.pub_pause = int(config['Export_params']['pub_pause'])
        self.delay_between_messages = int\
                (config['Export_params']['delay_between_messages'])
        """
        Создание логера, по умолчанию логируется все (INFO)
        Путь к лог файлу лежит в конфигах
        """
        logging.basicConfig\
                (filename=log_file,\
               encoding='utf-8', level=logging.INFO)

        """
        Создается обьект базы данных
        Сам класс лежит в файле news.py
        """
        self.db = Database(config['Database']['Path'])
        """
        Создается класс Источник
        Лежит в news.py
        В конфиге указаны все ссылки на RSS каналы, которые парсим 
        """
        self.src = Source(config['RSS'])
    
    def detect(self):
        news = self.src.news
        news.reverse()
        lemma = Lemma()
        for n in news:
            if not self.db.find_link(n.link):
                logging.info( u'Detect news: %s' % n)
                self.db.add_news(n)
            

def main():
    b = Bot() 
    b.detect()
    
if __name__ == '__main__':
    main()
