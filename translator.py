import asyncio
import async_google_trans_new


class Interpreter:
    """ For translation from string and list use translate() method

    Examples
    ----------
    some_translation = Interpreter()
    some_translate.translate("London is the capital of Great Britain")
    "Лондон - столица Великобритании"

    some_translation.translate("Beatles", "Scorpions", "Blur", "Sandy goes on vacation")
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

    def translate(self, input_):
        loop = asyncio.get_event_loop()
        if isinstance(input_, str) == True:
            return loop.run_until_complete(self.translate_from_string(input_))
        if isinstance(input_, list) == True:
            return loop.run_until_complete(self.translate_from_list(input_))
