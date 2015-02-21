__author__ = 'kotov'

import unittest


class TestWordCounter(unittest.TestCase):
    def should_load_stop_words(self):
        from WordCounter import WordCounter

        wordcounter = WordCounter()
        wordcounter.loadstopwords()
        self.assertEqual(True, len(wordcounter.stopWords) > 0)


if __name__ == '__main__':
    unittest.main()
