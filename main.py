import os
import re
import nltk
import genanki
import random
from mtranslate import translate
from nltk import PorterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

porter = PorterStemmer
snowball_stem = SnowballStemmer('english')
lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
nltk.download('stopwords')
FIND_DIRECTORY = "Files"


def walk(directory):
    for root, dirs, files in os.walk(directory):
        for name in files:
            file = os.path.join(root, name)
            with open(file, 'r', encoding='utf-8') as f:
                data = f.read()
                to_anki(name=name, map=translator(analysis_new(data), "ru"))
            f.close()


def analysis(text):
    frequency = {}
    matches = re.findall(r'\b[a-z]+\b', text, re.IGNORECASE)
    for word in matches:
        word = lemmatizer.lemmatize(word)
        if frequency.get(word) is None:
            frequency[word] = 1
        else:
            frequency[word] += 1
    frequency_sorted = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    return frequency_sorted


def analysis_new(text):
    word_set = set()
    word_list = []
    matches = re.findall(r'\b[a-z]+\b', text, re.IGNORECASE)
    for word in matches:
        word_set.add(word)
    for word in word_set:
        if word not in stopwords.words("english"):
            word_list.append(word)
    return word_list


def translator(list, lang):
    translate_map = {}
    end = len(list)
    cur = end
    for item in list:
        print(f'{cur} / {end}')
        translate_map[item.capitalize()] = translate(item.capitalize(), lang, "auto")
        cur -= 1
    for key in translate_map.keys():
        print(f'{key}  :  {translate_map[key]}')
    return translate_map


def to_anki(name, map):
    print("Model generate")
    my_model = genanki.Model(
        random.randint(0, 9999999),
        "Translate words",
        fields=[
            {'name': "Question"},
            {'name': "Answer"}
        ],
        templates=[
            {
                'name': "Card 1",
                'qfmt': '{{Question}}',
                'afmt': '<hr id="answer">{{Answer}}'
            }
        ]

    )
    print("Deck generate")
    my_deck = genanki.Deck(
        random.randint(0, 9999999),
        f'{name}'
    )
    print("Pushing card to deck")
    for key in map.keys():
        my_deck.add_note(genanki.Note(
            model=my_model,
            fields=[key, map[key]]
        ))
    print("Write to file")
    genanki.Package(my_deck).write_to_file(f'Output/{name}.apkg')


if __name__ == "__main__":
    walk(FIND_DIRECTORY)
