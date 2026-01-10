from natasha import Segmenter, NewsEmbedding, NewsSyntaxParser, Doc
from nltk import sent_tokenize

text = open('C:/учеба/Лингвистика/датасет.txt', encoding='utf-8').read()
sentences = sent_tokenize(text)[:5]
segmenter = Segmenter()
emb = NewsEmbedding()
parser = NewsSyntaxParser(emb)


def projective(tokens):
    pos = {t.id: i for i, t in enumerate(tokens)}
    deps = [(pos[t.id], pos[t.head_id]) for t in tokens if t.head_id != '0' and t.head_id in pos]

    for i, (a1, b1) in enumerate(deps):
        for a2, b2 in deps[i + 1:]:
            if (a1 < a2 < b1 < b2) or (a2 < a1 < b2 < b1):
                return False
    return True

def constituency_detailed(tokens):
    root = None
    for token in tokens:
        if token.rel == 'root':
            root = token
            break
    if not root:
        return "[предложение ]"
    subjects = []
    objects = []
    oblique = []
    modifiers = []
    for token in tokens:
        if token.rel != 'punct' and token.id != root.id:
            if 'nsubj' in token.rel:
                subjects.append(token.text)
            elif token.rel in ['obj', 'iobj']:
                objects.append(token.text)
            elif token.rel == 'obl':
                oblique.append(token.text)
            elif token.rel in ['advmod', 'nmod']:
                modifiers.append(token.text)
            else:
                modifiers.append(token.text)
    result = "[преложение"
    if subjects:
        result += f" [сущ: {' '.join(subjects)}]"
    result += f" [сказуемое: {root.text}"
    if objects:
        result += f" [сущ: {' '.join(objects)}]"
    if oblique:
        result += f" [доп:  {' '.join(oblique)}]"
    if modifiers:
        result += f" [обст:   {' '.join(modifiers)}]"
    result += "]]"
    return result


for i, sent in enumerate(sentences, 1):
    doc = Doc(sent)
    doc.segment(segmenter)
    doc.parse_syntax(parser)
    print(f"\n{i}. Предложение: {sent}")
    print("Дерево зависимостей:")
    doc.sents[0].syntax.print()
    print("Отрезочное представление:")
    print(constituency_detailed(doc.tokens))
    print(f"Проективное: {projective(doc.tokens)}")
    print("-" * 50)