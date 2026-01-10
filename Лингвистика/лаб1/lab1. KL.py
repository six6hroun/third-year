from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
with open('C:/учеба/Лингвистика/датасет.txt', "r", encoding='utf-8') as file:
    text = file.read()

sents = sent_tokenize(text)
print ("Текст разделенный на предложения")
print (sents)

words = word_tokenize(text)
print ("Текст разделенный на слова")
print (words)

reg = [word.lower() for word in words]
print("Текст приведенный к нижнему регистру")
print(reg)

stop_words = set(stopwords.words('russian'))
new_text = [word for word in reg if not (word in stop_words)]
print("Текст с удаленными стоп-словами")
print(new_text)