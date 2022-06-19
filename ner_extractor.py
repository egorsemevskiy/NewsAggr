# !pip install -U spacy > /dev/null
# !python -m spacy download ru_core_news_md > /dev/null

import ru_core_news_md
import spacy

MODEL = 'ru_core_news_md'

class NerExtractor():
    """
    Abstract base class for NER extraction.

    Input
    -----
    text : str
        Simple sentence.

    Returns
    -------
    Three NER tokens groups: set(list, list, list)
        ([PER_LIST], [LOC_LIST], [ORG_LIST])

    Examples
    --------
    text = 'Владимир Путин приехал сегодня в Москву'
    NER_model = NerExtractor(MODEL)
    NER_model.fit_transform(text)

    Output
    ------
    ([Владимир Путин], [Москву], [])

    """
    def __init__(self, model):
        self.nlp = spacy.load(model)
        self.PER = []
        self.LOC = []
        self.ORG = []

    def fit_transform(self, text):
        self.doc = self.nlp(text)

        for named_entity in self.doc.ents:
            if named_entity.label_ == 'PER':
                self.PER.append(named_entity)
            elif named_entity.label_ == 'LOC':
                self.LOC.append(named_entity)
            elif named_entity.label_ == 'ORG':
                self.ORG.append(named_entity)

        return self.PER, self.LOC, self.ORG
