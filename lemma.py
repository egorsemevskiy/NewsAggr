from natasha import (
            Segmenter,
            MorphVocab,
            NewsEmbedding,
            NewsMorphTagger,
            NewsSyntaxParser,
            NewsNERTagger,
            PER,
            LOC,
            NamesExtractor,
            Doc
             )

def main():
    segmenter = Segmenter()
    morph_vocab = MorphVocab()

    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    ner_tagger = NewsNERTagger(emb)

    names_extractor = NamesExtractor(morph_vocab)

    text = 'Посол Израиля на Украине Йоэль Лион признался, что пришел в шокa'
    doc = Doc(text)

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)

    for span in doc.spans:
        span.normalize(morph_vocab)


    for span in doc.spans:
        if span.type == LOC:
            span.extract_fact(names_extractor)
            print(span.normal) 


main()
