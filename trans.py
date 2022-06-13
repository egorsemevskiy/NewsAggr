import asyncio
import time
from googletrans import Translator
import async_google_trans_new

class Trans():
    
    def __init__(self):
        self.translator = Translator()

    def translate_titles(self, title):
        translation = self.translator.translate(text=title, dest='ru',src='auto')
        return translation
