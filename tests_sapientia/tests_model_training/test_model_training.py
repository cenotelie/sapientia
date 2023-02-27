import unittest

from sapientia.nlp.nlp import load_model, apply_model, named_entity_recognition


class TestModelTraining(unittest.TestCase):
    def test_load_trained_model(self):
        nlp = load_model("model/model-best")
        doc = apply_model(nlp, "Obama was born in Hawaii and was never involved in building EMEA.")
        ner = named_entity_recognition(doc)
        print(ner)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
