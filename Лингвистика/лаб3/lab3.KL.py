from natasha import Segmenter, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, Doc
with open('C:/учеба/Лингвистика/датасет.txt', "r", encoding='utf-8') as file:
    text = file.read()

segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)

doc = Doc(text)
doc.segment(segmenter)
doc.tag_morph(morph_tagger)
doc.parse_syntax(syntax_parser)
for i, sent in enumerate(doc.sents):
    print(f"Предложение {i + 1}: {sent.text}")
    print("Синтаксический разбор:")

    for token in sent.tokens:
        print(f"  {token.text} - {token.pos} ({token.rel})")

    print("Дерево зависимостей:")
    sent.syntax.print()
    print("\n")