# !pip install transformers > /dev/null
# !pip install torch

import torch
from transformers import AutoModelForSequenceClassification, BertTokenizer

MODEL_NAME = 'cointegrated/rubert-base-cased-dp-paraphrase-detection'
MODEL = AutoModelForSequenceClassification.from_pretrained(model_name)
TOKENIZER = BertTokenizer.from_pretrained(model_name)

class BertSimilarity():
    """
    Abstract base class for text classifier as paraphrases (class 1) 
    or non-paraphrases (class 0).

    Input
    -----
    text1 : str
        First sentence.
    text2 : str
        Second sentence.

    Returns
    -------
    raw_predictions: numpy.ndarray
        p(non-paraphrase), p(paraphrase)

    Examples
    --------
    text1 = 'В США признали чудовищную ошибку в отношении Путина'
    text2 = 'Американцы согласились что недооценили президента РФ'

    model = BertSimilarity(MODEL_NAME, MODEL, TOKENIZER)
    model.similatiry(text1, text2)[1]

    Output
    ------
    0.4244485

    The higher the score, the more likely it is the same
    """
    def __init__(self, model_name, model, tokenizer):
        self.model_name = model_name
        self.model = model
        self.tokenizer = tokenizer

    def similatiry(self, text1, text2):
        batch = self.tokenizer(text1, text2, return_tensors='pt')#.to(model.device)
        with torch.inference_mode():
            proba = torch.softmax(self.model(**batch).logits, -1).cpu().numpy()
        return proba[0]
