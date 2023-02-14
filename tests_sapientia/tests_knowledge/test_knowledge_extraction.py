import unittest

from sapientia.knowledge.knowledge_extraction import requirements_extraction, get_abbreviations


class TestKnowledgeExtraction(unittest.TestCase):
    def test_requirements_extraction(self):
        sentences = ["This is a sentence without any requirement.", "The code must be documented.",
                     "The code will be tested"]
        requirements = requirements_extraction(sentences)
        print(requirements)
        self.assertEqual(requirements, ['The code must be documented.', 'The code will be tested'])

    def test_get_abbreviations(self):
        abbreviations_file = "abbreviations.csv"
        abbreviations = get_abbreviations(abbreviations_file)
        print(abbreviations)
        print(abbreviations["EMA"])
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
