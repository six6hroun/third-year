from nltk import word_tokenize
from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer
RUSSIAN_TAGS = {
    'NOUN': 'существительное',
    'ADJF': 'прилагательное (полное)',
    'ADJS': 'прилагательное (краткое)',
    'COMP': 'компаратив',
    'VERB': 'глагол',
    'INFN': 'инфинитив',
    'PRTF': 'причастие (полное)',
    'PRTS': 'причастие (краткое)',
    'GRND': 'деепричастие',
    'NUMR': 'числительное',
    'ADVB': 'наречие',
    'NPRO': 'местоимение',
    'PRED': 'предикатив',
    'PREP': 'предлог',
    'CONJ': 'союз',
    'PRCL': 'частица',
    'INTJ': 'междометие',
    'nomn': 'именительный',
    'gent': 'родительный',
    'datv': 'дательный',
    'accs': 'винительный',
    'ablt': 'творительный',
    'loct': 'предложный',
    'voct': 'звательный',
    'sing': 'единственное',
    'plur': 'множественное',
    'masc': 'мужской',
    'femn': 'женский',
    'neut': 'средний',
    'anim': 'одушевленное',
    'inan': 'неодушевленное',
    'pres': 'настоящее',
    'past': 'прошедшее',
    'futr': 'будущее',
    'indc': 'изъявительное',
    'impr': 'повелительное',
    'perf': 'совершенный',
    'impf': 'несовершенный',
    'actv': 'действительный',
    'pssv': 'страдательный',
    '1per': '1 лицо',
    '2per': '2 лицо',
    '3per': '3 лицо',
    'None': 'не указано'
}

def translate_tag(tag, value):
    """Переводит тег на русский язык"""
    if value is None:
        return 'не указано'
    return RUSSIAN_TAGS.get(str(value), str(value))


with open('C:/учеба/Лингвистика/датасет.txt', "r", encoding='utf-8') as file:
    text = file.read()

words = word_tokenize(text)
print("Текст разделенный на слова")
print(words, "\n")

reg = [word.lower() for word in words]

stop_words = set(stopwords.words('russian'))
new_text = [word for word in reg if word.isalpha() and word not in stop_words]
print("Текст с удаленными стоп-словами")
print(new_text, '\n')

morph = MorphAnalyzer()
for word in new_text:
    print("=" * 50)
    p = morph.parse(word)[0]
    print("Слово:", word)
    print("Начальная форма:", p.normal_form)
    print("Часть речи:", translate_tag('POS', p.tag.POS))
    print("\nМОРФОЛОГИЧЕСКИЙ РАЗБОР:")
    print(f"- Часть речи: {translate_tag('POS', p.tag.POS)}")
    print(f"- Одушевленность: {translate_tag('animacy', p.tag.animacy)}")
    print(f"- Вид: {translate_tag('aspect', p.tag.aspect)}")
    print(f"- Падеж: {translate_tag('case', p.tag.case)}")
    print(f"- Род: {translate_tag('gender', p.tag.gender)}")
    print(f"- Наклонение: {translate_tag('mood', p.tag.mood)}")
    print(f"- Число: {translate_tag('number', p.tag.number)}")
    print(f"- Лицо: {translate_tag('person', p.tag.person)}")
    print(f"- Время: {translate_tag('tense', p.tag.tense)}")
    print(f"- Переходность: {translate_tag('transitivity', p.tag.transitivity)}")
    print(f"- Залог: {translate_tag('voice', p.tag.voice)}")

    gent_form = p.inflect({'gent'})
    plur_gent_form = p.inflect({'plur', 'gent'})
    print(f"\nСКЛОНЕНИЕ:")
    print(f"- Родительный падеж: {gent_form.word if gent_form else 'нет формы'}")
    print(f"- Мн. число, род. падеж: {plur_gent_form.word if plur_gent_form else 'нет формы'}")

    print(f"\nФОРМЫ С ЧИСЛИТЕЛЬНЫМИ:")
    form1 = p.make_agree_with_number(1)
    form2 = p.make_agree_with_number(2)
    form5 = p.make_agree_with_number(5)
    print(f"- С числительным 1: {form1.word if form1 else 'нет формы'}")
    print(f"- С числительным 2: {form2.word if form2 else 'нет формы'}")
    print(f"- С числительным 5: {form5.word if form5 else 'нет формы'}")

    print("=" * 50)
    print("\n")