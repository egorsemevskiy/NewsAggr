from natasha import (
            Segmenter,
            MorphVocab,
            NewsEmbedding,
            NewsMorphTagger,
            NewsSyntaxParser,
            NewsNERTagger,
            LOC,
            NamesExtractor,
            Doc
             )
class Lemma():

    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()

        self.morph_tagger = NewsMorphTagger(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)
        self.names_extractor = NamesExtractor(self.morph_vocab)

    def country_lemma(self , txt):

        doc = Doc(txt)

        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.tag_ner(self.ner_tagger)

        for span in doc.spans:
            span.normalize(self.morph_vocab)


        for span in doc.spans:
            if span.type == LOC:
                span.extract_fact(self.names_extractor)
                print(span.normal) 


