import unittest

from sapientia.nlp.nlp import load_model, apply_model, tokenize, named_entity_recognition


class TestNLP(unittest.TestCase):

    def test_tokenize(self):
        model = "en_core_web_sm"
        text = "Apple is looking at buying U.K. startup for $1 billion"
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        tokens = tokenize(doc)
        self.assertEqual(len(tokens), 11)
        self.assertEqual(tokens[0]["text"], "Apple")

    def test_named_entity_recognition(self):
        model = "en_core_web_sm"
        text = "Apple is looking at buying U.K. startup for $1 billion"
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        print(named_entities)
        self.assertEqual(len(named_entities), 3)
        self.assertEqual(named_entities[0]["text"], "Apple")
        self.assertEqual(named_entities[0]["start_char"], 0)
        self.assertEqual(named_entities[0]["end_char"], 5)
        self.assertEqual(named_entities[0]["label"], "ORG")


if __name__ == '__main__':
    unittest.main()
