__author__ = 'kotov'

import unittest


class TestWordCounter(unittest.TestCase):
    def should_load_stop_words(self):
        from WordCounter import load_stop_words

        words = load_stop_words()
        self.assertEqual(True, len(words) > 0)


if __name__ == '__main__':
    unittest.main()
