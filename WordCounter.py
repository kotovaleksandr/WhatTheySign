__author__ = 'kotov.a'

import operator
import os


def load_stop_words():
    files = (element for element in os.listdir('stopwords') if element.endswith('txt'))
    result = []
    for file in files:
        lines = open('stopwords/' + file).readlines()
        lines = [line.strip() for line in lines]

        result += lines
    return result


def sort_dictionary_by_value(words):
    return sorted(words.items(), key=operator.itemgetter(1), reverse=True)


class WordCounter:
    def __init__(self):
        self.stopWords = load_stop_words()

    def count_popular_words(self, text, result):
        words = text.replace('...', ' ').replace(',', ' ').replace('.', ' ').replace('?', ' '). \
            replace(';', ' ').replace('!', ' ').replace('\"', ' ').split(' ')
        words = set(words)
        filtered = (word for word in words if
                    word and word != '' and word != '\'' and not word.isspace() and word not in self.stopWords)
        for word in filtered:
            if result.__contains__(word):
                result[word] += 1
            else:
                result[word] = 1
        return result