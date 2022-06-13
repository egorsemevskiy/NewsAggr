from bs4 import BeautifulSoup
import requests
import asyncio
import time
from googletrans import Translator
import async_google_trans_new


class Interpreter:

    def __init__(self, url):
        self.url = url
        self.titles = None
        self.list_ = None

    def get_titles(self):
        response = requests.get(self.url)
        response = response.text
        soup = BeautifulSoup(response, "html.parser")
        # либо оставляем html.parser либо надо ставить ещё дополнительную депенденси в виде pip install xml
        titles = soup.findAll('title')
        titles = [str(title).replace(' &gt;', "").replace('<title>', "").replace('</title>', "").replace('NYT', "")
                  for title in titles]
        self.titles = list(set(titles))
        print(self.titles)

    def translate_titles(self):
        self.list_ = []
        translator = Translator()
        for title in self.titles:
            translation = translator.translate(text=title, dest='ru', src='auto')
            self.list_.append(translation.text)
        print(f"finished at {time.strftime('%X')}")

    async def async_translate_titles(self):
        g = async_google_trans_new.AsyncTranslator()
        list_ = []
        for title in self.titles:
            list_.append(g.translate(title, "ru"))
        self.list_ = await asyncio.gather(*list_)

    def translation_to_file(self):
        with open("translated.txt", 'w') as file:
            for item in self.list_:
                file.write(item + "\n")
        with open("original.txt", "w", encoding="utf-8") as file:
            for title in self.titles:
                file.write(title + "\n")


if __name__ == '__main__':
    print(f"started at {time.strftime('%X')}")
    URL = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
    some_interp = Interpreter(URL)
    some_interp.get_titles()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(some_interp.async_translate_titles())
    loop.close()
    some_interp.translation_to_file()
    print(f"finished at {time.strftime('%X')}") 
