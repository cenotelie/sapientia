import unittest

from sapientia.nlp.nlp import load_model, apply_model, named_entity_recognition


class TestModelTraining(unittest.TestCase):
    def test_load_trained_model(self):
        nlp = load_model("models/collins_en")
        doc = apply_model(nlp, "EMEA is provided by the supplier. It is composed by a chipset and a board.")
        ner = named_entity_recognition(doc)
        print(ner)
        self.assertEqual(ner[0]["text"], "EMEA")  # add assertion here


if __name__ == '__main__':
    unittest.main()
