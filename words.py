from navec import Navec
from slovnet import NER
from natasha import ( Segmenter,
        MorphVocab,
        LOC,
        AddrExtractor,
        Doc,
        NewsNERTagger,
        NewsEmbedding)

text ='В России за сутки госпитализировали 819 человек с короновирусом'

def main():
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    addr_extractor = AddrExtractor(morph_vocab)

    emb = NewsEmbedding()
    ner_tagger = NewsNERTagger(emb)

    doc = Doc(text)

    #matches = addr_extractor(text)


    doc.segment(segmenter)
    print(doc.tokens[:5])

main()

