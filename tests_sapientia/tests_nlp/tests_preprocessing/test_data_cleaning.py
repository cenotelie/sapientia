import unittest

from sapientia.nlp.preprocessing.data_cleaning import sentences_fixing, group_lists_in_sentences, sentences_cleaning


class TestDataCleaning(unittest.TestCase):

    def test_sentences_fixing(self):
        sentences = ["This is a sentence e.g.", "cut in half.", "This is another sentence", "Take this sentence",
                     "This is the last sentence and it is e.g.", "also cut in half"]
        fixed_sentences = sentences_fixing(sentences)
        self.assertEqual(fixed_sentences, ['This is a sentence e.g. cut in half.', 'This is another sentence',
                                           'Take this sentence',
                                           'This is the last sentence and it is e.g. also cut in half'])

    def test_group_lists_in_sentences(self):
        sentences = ["This is a sentence", "this is the beginning of a list :", "• first item", "• second item",
                     "This is another sentence"]
        grouped_sentences = group_lists_in_sentences(sentences)
        self.assertEqual(grouped_sentences, ['This is a sentence',
                                             'this is the beginning of a list : • first item • second item',
                                             'This is another sentence'])

    def test_sentences_cleaning(self):
        sentences = ["", ", ", "Page 5 of 965  1 apple, please.", " \n This is a sentence"]
        cleaned_sentences = sentences_cleaning(sentences)
        self.assertEqual(cleaned_sentences, ['1 apple, please.', 'This is a sentence'])


if __name__ == '__main__':
    unittest.main()
