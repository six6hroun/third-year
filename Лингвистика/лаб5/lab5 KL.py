from natasha import Segmenter, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, Doc
import pymorphy3 as pm
from graphviz import Digraph
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
sentences = [
    "В немноголюдном парке царит особая атмосфера спокойствия",
    "Свежий воздух наполнен ароматом распустившихся цветов",
    "Лёгкий ветер колышет ветви деревьев, создавая приятную прохладу",
    "Спококойная гладь пруда отражает утреннее небо",
    "Тишина изредка нарушается шелестом листвы"
]

def nid(t):
    try:
        _, x = map(int, t.split('_'))
        return x
    except:
        return 0

def s2d(s):
    w = {}
    r = None
    for tok in s.tokens:
        if tok.pos != 'PUNCT':
            i = nid(tok.id)
            w[i] = tok.text
            if tok.rel == 'root':
                r = i
    if r is None and w:
        r = list(w.keys())[0]

    tr = {k: [] for k in w.keys()}
    for t in s.tokens:
        if t.pos != 'PUNCT':
            i = nid(t.id)
            h = nid(t.head_id)
            if h != 0 and h in tr:
                tr[h].append(i)
    return w, r, tr


ma = pm.MorphAnalyzer()
def lem(x):
    try:
        return ma.parse(x)[0].normal_form
    except:
        return x


def d2r(w, r, tr):
    if len(w) <= 1:
        return list(w.values())

    rp = []
    st = [(0, r)]
    col = {k: 0 for k in w.keys()}

    while st:
        p, c = st[-1]
        if col[c] == 0:
            col[c] = 1
            for nx in reversed(tr.get(c, [])):
                if col.get(nx, 0) == 0:
                    st.append((c, nx))
        else:
            if len(tr.get(c, [])) > 1:
                rp.extend(['*', len(tr[c])])

            if c != r:
                if len(tr.get(c, [])) == 0:
                    rp.extend([w[c], w[p], '*'])
                else:
                    rp.extend([w[p], '*'])

            st.pop()

    return rp


def r2ss(rp):
    if len(rp) <= 1:
        return rp

    ss = []
    wrk = rp.copy()
    i = 0

    while i < len(wrk):
        if wrk[i] == '*':
            if i + 1 < len(wrk) and isinstance(wrk[i + 1], int):
                n = wrk[i + 1]
                m = 2
            else:
                n = 2
                m = 1

            if i >= n:
                if m == 2:
                    r = ' '.join(map(str, wrk[i - n:i + m]))
                    wrk[i - n:i + m] = [r]
                    ss.append(r)
                    i -= n
                else:
                    r = ' '.join(map(str, wrk[i - n:i + m]))
                    wrk[i - n:i + m] = [r]
                    ss.append(r)
                    i -= n
        i += 1
    return ss


def s2ss(s):
    w, r, tr = s2d(s)
    for k in list(w.keys()):
        w[k] = lem(w[k])
    rp = d2r(w, r, tr)
    ss = r2ss(rp.copy())
    return rp, ss


def viz(s, k='dep', fn='tree', dr='TB', lm=True, rn=True):
    d = Digraph(comment=f'{k} tree', format='png')
    d.attr(rankdir=dr, splines='polyline', nodesep='0.35', ranksep='0.6')
    d.attr('node', shape='circle', fontname='Arial', fontsize='12')
    d.attr('edge', fontname='Arial', fontsize='10')
    if k == 'dep':
        w, r, tr = s2d(s)
        if lm:
            for kx in list(w.keys()):
                w[kx] = lem(w[kx])
        for kx, wx in w.items():
            d.node(str(kx), wx)
        root_added = False
        for p, chs in tr.items():
            for ch in chs:
                if p == 0:
                    if not root_added:
                        d.node('ROOT', 'ROOT', shape='plaintext', fontsize='10')
                        root_added = True
                    d.edge('ROOT', str(ch))
                else:
                    d.edge(str(p), str(ch))
    elif k == 'ss':
        w, r, tr = s2d(s)
        if lm:
            for kx in list(w.keys()):
                w[kx] = lem(w[kx])
        rp = d2r(w, r, tr)

        for kx in sorted(w.keys()):
            txt = w[kx]
            nid2 = f'w_{kx}'
            d.node(nid2, txt)

        stack = []
        node_counter = 1
        word_nodes = {f'w_{k}': w[k] for k in sorted(w.keys())}

        i = 0
        while i < len(rp):
            item = rp[i]
            if isinstance(item, str) and item != '*':
                stack.append(f'w_{list(w.keys())[list(w.values()).index(item)]}')
            elif item == '*':
                if i + 1 < len(rp) and isinstance(rp[i + 1], int):
                    n = rp[i + 1]
                    i += 1
                else:
                    n = 2

                if len(stack) >= n:
                    children = stack[-n:]
                    stack = stack[:-n]

                    node_id = f'r_{node_counter}'
                    node_counter += 1

                    d.node(node_id, node_id, xlabel=f'*{n}' if n > 2 else '*')

                    for child in children:
                        d.edge(child, node_id)

                    stack.append(node_id)
            i += 1

    else:
        raise ValueError('k должно быть "dep" или "ss"')

    if rn:
        try:
            d.render(fn, cleanup=True)
            print(f"Создан файл: {fn}.png")
        except Exception as e:
            print(f"Ошибка при создании {fn}.png: {e}")
    return d

seg = Segmenter()
emb = NewsEmbedding()
mt = NewsMorphTagger(emb)
sp = NewsSyntaxParser(emb)

print("Начало обработки предложений...")

for i, sentence in enumerate(sentences, 1):
    print(f"\n{'=' * 60}")
    print(f"Предложение {i}: {sentence}")
    print(f"{'=' * 60}")

    try:
        doc = Doc(sentence)
        doc.segment(seg)
        doc.tag_morph(mt)
        doc.parse_syntax(sp)

        if not doc.sents:
            print("Не удалось разобрать предложение")
            continue

        sent_obj = doc.sents[0]

        w, r, tr = s2d(sent_obj)
        print(f"Слова: {w}")
        print(f"Корень: {r}")
        print(f"Дерево: {tr}")

        for k in list(w.keys()):
            w[k] = lem(w[k])

        rp = d2r(w, r, tr)
        ss = r2ss(rp.copy())

        print('ОПЗ функционала смысла:')
        print(' '.join(map(str, rp)))
        print('Фрагменты функционала смысла:')
        for x in ss:
            print(' ', x)

        viz(sent_obj, k='dep', fn=f'sentence_{i}_dep', dr='TB')
        viz(sent_obj, k='ss', fn=f'sentence_{i}_ss', dr='LR')

    except Exception as e:
        print(f"Ошибка при обработке предложения {i}: {e}")
        continue

print("\nОбработка завершена!")