import asyncio
import async_google_trans_new


class Interpreter:
    """ For translation from string use
    translate_from_string method with string as input

    For translation from list use
    translate_from_list method with list as input

    Examples
    ----------
    some_translation = Interpreter()
    some_translate.translate_from_string("London is the capital of Great Britain")
    "Лондон - столица Великобритании"

    some_translation.translate_from_list("Beatles", "Scorpions", "Blur", "Sandy goes on vacation")
    ['Битлз ', 'Скорпионы ', 'Размытие ', 'Сэнди уходит в отпуск ']
    """

    def __init__(self):
        self.titles = None
        self.list_ = None

    async def translate_from_string(self, text: str = 'house') -> str:
        g = async_google_trans_new.AsyncTranslator()
        translate_ = await g.translate(text, "ru")
        return translate_

    async def translate_from_list(self, texts_: list) -> list:
        list_ = []
        for text in texts_:
            list_.append(self.translate_from_string(text))
        list_ = await asyncio.gather(*list_)
        return list_


# if __name__ == '__main__':
#     STRING = "There is a sparrow on my kitchen"
#     with open("original.txt", "r", encoding="utf-8") as file:
#         texts = file.read()
#     texts = [text for text in texts.splitlines()]
#     some_interp = Interpreter()
#     loop = asyncio.get_event_loop()
#     # translate = loop.run_until_complete(some_interp.translate_from_string)
#     translate = loop.run_until_complete(some_interp.translate_from_string(STRING))
#     print(translate)
#     translate = loop.run_until_complete(some_interp.translate_from_list(texts))
#     print(translate)

