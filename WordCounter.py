__author__ = 'kotov'

import operator
import os


class WordCounter:
    def __init__(self):
        self.stopWords = self.loadstopwords()

    def countpopularwords(self, text, result):
        words = text.replace('...', ' ').replace(',', ' ').replace('.', ' ').replace('?', ' '). \
            replace(';', ' ').replace('!', ' ').replace('\"', ' ').split(' ')
        words = set(words)
        filtered = (word for word in words if
                    word and word != '' and word != '\'' and not word.isspace() and word not in self.stopWords)
        for word in filtered:
            # print(word, words.count(word))
            # word = bytes(word, 'utf8').decode("unicode_escape")
            # word = str(word).lower().strip()
            # if word in self.stopWords:
            # continue
            #print(word)
            if result.__contains__(word):
                result[word] += 1
            else:
                result[word] = 1
        return result

    def printordered(self, words):
        ordered = sorted(words.items(), key=operator.itemgetter(1), reverse=True)

        for word in ordered:
            print(word)

    def sortdictionarybyvalue(self, words):
        return sorted(words.items(), key=operator.itemgetter(1), reverse=True)

    def loadstopwords(self):
        files = (element for element in os.listdir('stopwords') if element.endswith('txt'))
        result = []
        for file in files:
            lines = open('stopwords/' + file).readlines()
            lines = [line.strip() for line in lines]

            result += lines
        return result
